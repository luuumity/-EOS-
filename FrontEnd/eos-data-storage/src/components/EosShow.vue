<template>
  <div id="EosShow" style="height: auto; display: grid; place-items: center">
    <div></div>
    <div>
      数据ID:
      <el-input
        placeholder="请输入数据ID"
        v-model="inputDataId"
        clearable
        style="
          width: 400px;
          margin-top: 35px;
          margin-right: 50px;
          margin-bottom: 35px;
        "
      >
      </el-input>
    </div>

    <el-button type="primary" icon="el-icon-download" @click="download_data"
      >搜索</el-button
    >
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "EosShow",
  data() {
    return {
      inputDataId: "",
    };
  },
  methods: {
    downloadFile(content, filename) {
      let a = document.createElement("a");
      a.href = content;
      a.download = filename;
      a.click();
    },
    download_data() {
      var eos_show = this;
      axios
        .post(
          "http://192.168.1.110:5000/eos/uploaddata/api/show",
          {
            dataID: eos_show.inputDataId,
          },
          { responseType: "blob" }
        )
        .then(function (response) {
          console.log(response);
          console.log(response.headers["content-disposition"]);
          var filename = response.headers["content-disposition"];
          console.log(response.headers["show-result"])
          if (response.headers["show-result"] == "2") {
            alert('查询失败, 无此数据ID对应的文件!')
            return;
          } else {
            let blob = response.data;
            let objectUrl = URL.createObjectURL(blob); //生成一个url
            eos_show.downloadFile(objectUrl, filename);
            alert('查询成功, 文件已下载到本地!')
          }
        });
    },
  },
};
</script>

<style>
</style>