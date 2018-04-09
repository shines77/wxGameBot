
import re

def re_test():
    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123 456 789')
    print(result)
    
    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123,456,789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123;456;789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123:456:789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123~456~789')
    print(result)
    
    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123!456!789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123@456@789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123#456#789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123$456$789')
    print(result)
    
    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123%456%789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123^456^789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123*456*789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123?456?789')
    print(result)
    
    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123&456&789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123.456.789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\'456\'789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\"456\"789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\t456\t789')
    print(result)
    
    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\v456\v789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\f456\f789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\r456\r789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\n456\n789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123|456|789')
    print(result)
    
    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123\\456\\789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123/456/789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123,456 789')
    print(result)

    result = re.split(r'[ ,;:~!@#\$\%\^&\*\?\.\'\"\t\v\f\r\n|\\/]', '123，456,789')
    print(result)

if __name__ == "__main__":
    re_test()
            