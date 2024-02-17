<template>
  <div id="app" style="height: auto">
    <el-container style="height: 800px; border: 5px solid #eee">
      <el-header style="text-align: center; font-size: 20px">
        <span>EOS区块链的可信存证系统</span>
      </el-header>
      <el-container>
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
          <el-menu>
            <el-menu-item @click="switchPage(1)">上传文件</el-menu-item>
            <!-- <el-menu-item @click="switchPage(2)">更新文件</el-menu-item> -->
            <el-menu-item @click="switchPage(3)">搜索文件</el-menu-item>
            <!-- <el-menu-item @click="switchPage(4)">删除文件</el-menu-item> -->
          </el-menu>
        </el-aside>

        <el-container>
          <el-main>
            <eos-upload v-show="indexPage === 1 && isShowPage"></eos-upload>
            <!-- <eos-updata v-show="indexPage === 2 && isShowPage"></eos-updata> -->
            <eos-show v-show="indexPage === 3 && isShowPage"></eos-show>
            <!-- <eos-remove v-show="indexPage === 4 && isShowPage"></eos-remove> -->
          </el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import EosUpload from "./components/EosUpload.vue";
import EosShow from "./components/EosShow.vue";
// import EosUpdata from "./components/EosUpdata.vue";
// import EosRemove from "./components/EosRemove.vue";

export default {
  name: "App",
  components: {
    EosUpload,
    EosShow,
    // EosUpdata,
    // EosRemove,
  },
  data() {
    return{
      indexPage : 1,
      isShowPage : true
    };
  },
  methods: {
    switchPage(index){
      this.indexPage = index
    }
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
