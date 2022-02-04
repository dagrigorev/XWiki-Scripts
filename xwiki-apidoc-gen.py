from ensurepip import version
import ssl, urllib.request, json, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    # Remove a file
    os.remove('api.xwiki') if os.path.exists('api.xwiki') else print ("Creating new specification...\n")

    # Open a file with access mode 'a'
    with open("api.xwiki", "a") as file_object:
        resource = urllib.request.urlopen("https://localhost:5001/swagger/v1/swagger.json", context=ctx)
        content =  resource.read().decode(resource.headers.get_content_charset())
        data = json.loads(content)
        print("Swagger specification is loaded\n" if data else "Cannot load swagger specification\n")
        
        api_version = data["info"]["version"]
        api_name = data["info"]["title"]

        file_object.write("{{toc/}}\n")
        file_object.write('==Описание API {name} {version}==\n'.format(name=api_name, version=api_version))

        file_object.write("\n")

        methods = data["paths"]
        for method_name in methods:
            for method_type in methods[method_name]:
                if('summary' in methods[method_name][method_type]):
                    file_object.write("==={summary}===\n".format(summary=methods[method_name][method_type]["summary"]))
                    file_object.write("\n\n")
                if('description' in methods[method_name][method_type]):
                    file_object.write("{description}\n".format(description=methods[method_name][method_type]["description"]))
                    file_object.write("\n")
                
                file_object.write("\n=====Метод:===== \n\n")
                file_object.write("{{code language=\"bash\"}}\n")
                file_object.write("[{mtype}] {method}\n".format(mtype=method_type.upper(), method=method_name))
                file_object.write("\n{{/code}}\n\n")
                
                file_object.write("=====Ответ:====== \n")
                file_object.write("\n{{code language=\"bash\"}}\n")
                file_object.write("\n# Добавить описание ответа\n\n")
                if('responses' in methods[method_name][method_type]):
                    json.dump(methods[method_name][method_type]["responses"], file_object, indent=4, separators=(',',': '))
                    file_object.write("\n")
                file_object.write("\n{{/code}}\n")

                if('parameters' in methods[method_name][method_type]):
                    file_object.write("\n=====Параметры:=====\n")
                    if(not methods[method_name][method_type]["parameters"]):
                        print("Отсутствуют\n")
                    else:
                        for param in methods[method_name][method_type]["parameters"]:
                            name = param["name"]
                            input_type = param["in"]
                            desc = param["description"] if "description" in param else ""
                            is_param_required = param["required"] if "required" in param else "False"

                            file_object.write("Название: // {paramName} //\n".format(paramName = name))
                            file_object.write("Тип передачи: {inputType}\n".format(inputType = input_type))
                            if(desc):
                                file_object.write("Описание: {paramDesc}\n".format(paramDesc = desc))
                            file_object.write("Параметр обязателен? - {required}\n".format(required=is_param_required))
                            file_object.write("-------------------------------------------------------------\n")
        file_object.flush()
        file_object.close()

        print("API documentation for XWiki is generated successfully!\n")
except Exception as ex:
    print("Error while generating API documentation for XWiki. Error argument: {error}\n\n".format(error=str(ex)))