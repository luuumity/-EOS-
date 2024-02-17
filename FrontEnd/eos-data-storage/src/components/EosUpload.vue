<template>
  <div id="EosUpload" style="height: auto; display: grid; place-items: center">
    <div>
      用户名:
      <el-input
        placeholder="请输入用户名"
        v-model="inputUserName"
        clearable
        style="width: 400px; margin-top: 35px; margin-right: 50px"
      >
      </el-input>
    </div>
    <div>
      数据ID:
      <el-input
        placeholder="请输入数据ID"
        v-model="inputDataId"
        clearable
        style="width: 400px; margin-top: 35px; margin-right: 50px"
      >
      </el-input>
    </div>
    <el-upload
      ref="upload"
      drag
      action="http://192.168.1.110:5000/eos/uploaddata/api/uploadedfiles"
      :multiple="false"
      :auto-upload="false"
      :limit="1"
      :http-request="upload_file"
      style="margin: 35px; width: 400px"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">
        <!-- 只能上传jpg/png文件,且不超过500kb -->
      </div>
    </el-upload>

    <el-button type="primary" icon="el-icon-upload2" @click="upload_data"
      >上传</el-button
    >
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "EosUpload",
  data() {
    return {
      msg: "",
      inputDataId: "",
      inputUserName: "",
    };
  },
  methods: {
    upload_file(files) {
      var eos_upload = this;
      var formData = new FormData();
      if (files.length !== 0) {
        formData.append("accountName", eos_upload.inputUserName);
        formData.append("dataID", eos_upload.inputDataId);
        formData.append("file", files.file, files.file.name);
      }
      axios
        .post("http://192.168.1.110:5000/eos/uploaddata/api/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(function (response) {
          if (response.data.msgNum == 1) {
            alert("上传成功!");
          } else {
            alert("上传失败!");
          }
        });
    },
    upload_data() {
      this.$refs.upload.submit();
    },
  },
};
</script>

<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>