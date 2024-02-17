#! usr/bin/python
# -* - coding: UTF-8 -* -

from glob import escape
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS

from base64 import b64encode, b64decode
import hashlib
import os, time

api_path = '/eos/uploaddata/api/'

app = Flask(__name__)
cors = CORS(app, resources={api_path + "*": {"origins": "*"}})


# 请求上传文件api
@app.route(api_path + 'upload', methods=['POST'])
def uploaddata_upload():
    # 拿到客户端传来的数据
    data = request.form

    # 拿到用户名'accountName', 数据ID'dataID', 上传文件'file'
    accountName = data['accountName']
    dataID = data['dataID']
    file = request.files['file']
    file_read = file.read()
    md5 = hashlib.md5()
    md5.update(file_read)
    file_hash_data = md5.digest()

    # 对字符串进行检查
    # TBD...

    # 对文件进行编码和组装, 最后转化为一个字符串'fileDataString'
    file_data = file_hash_data + b'0xffffffff' + bytes(file.filename, encoding = "utf8") + b'0xffffffff' + file_read

    fileDataString = b64encode(file_data).decode('utf-8')
    print(fileDataString)

    # 根据输入开始拼接eos命令'eos_cmd'
    eos_cmd = "cleos push action uploaddata upload '[\"" + accountName + "\", \"" + dataID + "\", \"" + fileDataString + "\"]' -p " + accountName + "@active"

    # 执行eos命令'eos_cmd'
    eos_cmd_resault = ''
    eos_cmd_resault = os.popen(eos_cmd).read()

    # 根据执行结果'eos_cmd_resault', 执行相应的代码
    switch_response = 2
    if eos_cmd_resault.find('>> ') >= 0:
        switch_response = 1

    # 根据执行结果, 给客户端发送相应数据
    # 执行成功:

    print(eos_cmd_resault.find('already'))

    if switch_response == 1:
        response = {
            'msgNum': 1,
            'msg': 'upload action succeed!'
        }

        return jsonify(response)

    # 执行失败:
    elif switch_response == 2:
        response = {
            'msgNum': 2,
            'msg': 'upload action fail!'
        }

        return jsonify(response)



# 请求下载文件api
@app.route(api_path + 'show', methods=['POST'])
def uploaddata_show():
    J_data = request.get_json()

    print(J_data)

    # 得到数据ID'dataID'
    dataID = J_data['dataID']

    # 拼接show操作的cmd
    eos_cmd = "cleos push action uploaddata show '[ " + dataID + "]' -p uploaddata@active"

    eos_cmd_resault = ''
    eos_cmd_resault = os.popen(eos_cmd).read()
    print('eos_cmd_res: ' + eos_cmd_resault)

    if  eos_cmd_resault.find('>>') == -1:
        response = make_response()
        response.headers['Access-Control-Expose-Headers'] = 'Show-Result'
        response.headers['Show-Result'] = '2'
        return response

    str = eos_cmd_resault.split('>> ')
    str = str[-1][:-1]

    file_decode = b64decode(str)

    file_of_bytes = file_decode.split(b'0xffffffff')


    file_hash = file_of_bytes[0]
    file_name = file_of_bytes[1].decode('utf-8')
    file_data = file_of_bytes[2]

    if (file_hash == hashlib.md5(file_data).digest()):
        return 

    file = open('./uploadfiles/' + file_name, 'wb+')
    file.write(file_data)
    file.close()

    # 返回链上的文件
    uploads = os.path.join(app.root_path, 'uploadfiles')
    response = make_response(send_from_directory(uploads, file_name, as_attachment=True))
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition, Show-Result'
    response.headers['Content-Disposition'] = file_name
    response.headers['Show-Result'] = '1'

    return response



# 请求更新文件api ***note: "this api is abandoned"***
@app.route(api_path + 'updata', methods=['POST'])
def uploaddata_updata():
    pass



# 请求删除文件api ***note: "this api is abandoned"***
@app.route(api_path + 'remove', methods=['POST'])
def uploaddata_remove():
    pass




# 启动运行
if __name__ == '__main__':


    print('-------------------------')
    # unlock wallet
    os.system('cleos wallet unlock << EOF PW5KAWpYtzh8dENLoLwWbPTFwULH8Z45qFjGUF7JppkfYF9yHXhhr EOF')

    app.run('0.0.0.0')   # 这样子会直接运行在本地服务器，也即是 localhost:5000
   # app.run(host='your_ip_address') # 这里可通过 host 指定在公网IP上运行