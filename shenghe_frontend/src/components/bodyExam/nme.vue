<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-setting"></i> 非会员录入
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-button icon="el-icon-circle-plus-outline"
          class="mr10"
          @click="addNew">新增</el-button>
        <el-input v-model="query.referee"
          placeholder="推荐人"
          class="handle-input1 mr10"></el-input>
        <el-select v-model="query.channel"
          placeholder="渠道"
          class="handle-select1 mr10">
          <el-option key="A"
            label="所有"
            value="A" />
          <el-option v-for="item in combox.channel"
            :key="item.code"
            :label="item.label"
            :value="item.code">
          </el-option>
        </el-select>
        <el-input v-model.number="query.age"
          type="number"
          placeholder="年龄"
          class="handle-input1 mr10">
        </el-input>
        <el-select v-model="query.sex"
          placeholder="性别"
          class="handle-select1 mr10">
          <el-option key="A"
            label="所有"
            value="A" />
          <el-option v-for="item in combox.sex"
            :key="item.code"
            :label="item.label"
            :value="item.code">
          </el-option>
        </el-select>
        <el-input v-model="query.name"
          placeholder="姓名"
          class="handle-input1 mr10">
        </el-input>
        <el-button type="primary"
          icon="el-icon-search"
          @click="findClick">
          搜索
        </el-button>
      </div>
      <el-row>
        <el-col :span="10">
          <!-- 表格 -->
          <el-table :data="tableData"
            border
            class="table"
            ref="itemTable"
            header-cell-class-name="table-header"
            @current-change="handleItemChange">
            <el-table-column prop="id"
              label="ID"
              width="55"
              align="center">
            </el-table-column>
            <el-table-column prop="referee"
              label="推荐人"
              width="100"
              align="center">
            </el-table-column>
            <el-table-column label="渠道"
              width="110">
              <template slot-scope="scope">
                {{ listToTextFormatter(combox.channel, scope.row.channel) }}
              </template>
            </el-table-column>
            <el-table-column prop="age"
              label="年龄"
              width="80"
              align="center">
            </el-table-column>
            <el-table-column label="性别"
              width="55">
              <template slot-scope="scope">
                {{ listToTextFormatter(combox.sex, scope.row.sex) }}
              </template>
            </el-table-column>
            <el-table-column prop="name"
              label="名字"
              align="center">
            </el-table-column>
          </el-table>
        </el-col>
        <el-col :span="14">
          <div class="form-box">
            <div class="title">{{ form.title }} </div>
            <el-form ref="form"
              :model="form"
              :rules="rules"
              label-width="180px">
              <el-form-item label="推荐人">
                <el-input v-model="form.referee"
                  ref="refReferrr"
                  placeholder="推荐人"
                  class="handle-input mr10"></el-input>
              </el-form-item>
              <el-form-item label="渠道"
                prop="name">
                <el-select v-model="form.channel"
                  placeholder="渠道"
                  class="handle-select mr10">
                  <el-option v-for="item in combox.channel"
                    :key="item.code"
                    :label="item.label"
                    :value="item.code">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="姓名"
                prop="name">
                <el-input v-model="form.name"
                  placeholder="姓名"
                  class="handle-input mr10"></el-input>
              </el-form-item>
              <el-form-item label="年龄"
                prop="age">
                <el-input v-model="form.age"
                  @blur="initItem"
                  type="number"
                  placeholder="年龄"
                  class="handle-input mr10"></el-input>
              </el-form-item>
              <el-form-item label="性别"
                prop="sex">
                <el-select v-model="form.sex"
                  @change="initItem">
                  <el-option v-for="item in combox.sex"
                    :key="item.code"
                    :label="item.label"
                    :value="item.code">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item v-for="(item) in form.items"
                :label="item.name+'('+item.value+')'"
                :key="item.id">
                <el-input v-model="item.score"
                  :placeholder="item.name"
                  class="handle-input mr10"></el-input>
              </el-form-item>
            </el-form>
            <div style="text-align: center">
              <el-button @click="reset">重新填写</el-button>
              <el-button type="primary"
                @click="saveClick">保存</el-button>
              <el-button type="primary"
                @click="showResult">查看结果报表</el-button>
            </div>
          </div>
        </el-col>
      </el-row>

    </div>
  </div>
</template>

<script>
import request from '@/utils/request.js';
export default {
  name: 'nsim',
  data () {
    return {
      query: {
        channel: '',
        referee: '',
        age: '',
        sex: '',
        name: ''
      },
      combox: {
        sex: [{
          code: 'M',
          label: '男性'
        }, {
          code: 'F',
          label: '女性'
        }],
        channel: []
      },
      form: { title: '新增信息', items: [] },
      tableData: [],
      rules: {        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ], sex: [
          { required: true, message: '请输入性别', trigger: 'blur' }
        ]      },
      contextPath: localStorage.getItem('backendContextPath')
    };
  },
  mounted () {
    this.init();
  },
  methods: {
    init () {
      request({
        url: this.contextPath + '/bc/api/channel',
        method: 'get',
      }).then(result => {
        this.combox.channel = result.map(data => {
          return { code: data[0], label: data[1] };
        });
        this.findClick();
      });
    },
    initItem () {
      if (this.form.age && this.form.sex) {
        request({
          url: this.contextPath + '/bc/nonmember/master',
          method: 'get',
          params: this.form
        }).then(data => {
          this.form.items = data;
        });
      }
    },
    addNew () {
      this.form = {
        title: '新增信息',
        items: []
      };
      this.$refs.refReferrr.focus();
    },
    findClick () {
      request({
        url: this.contextPath + '/bc/nonmember',
        method: 'get',
        params: this.query
      }).then(data => {
        this.tableData = data.map(item => {
          return { ...item, isSelected: false }
        });
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      })
    },
    saveClick () {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.doSave();
        } else {
          this.$message.error('输入项有误，请检查！');
          return false;
        }
      });
    },
    doSave () {
      let url = '/bc/nonmember/insert';
      return request({
        url: this.contextPath + url,
        method: 'post',
        data: this.form
      }).then(data => {
        this.$message.success('增加成功!');
        this.findClick();
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      });
    },
    reset () {
      this.form = { items: [] };
      this.$refs.refReferrr.focus();
    },
    handleItemChange (row) {
      this.form = {
        title: '查看信息',
        id: row.id,
        referee: row.referee,
        channel: row.channel,
        age: row.age,
        sex: row.sex,
        name: row.name,
        items: []
      };
      this.initItem();
      let url = '/bc/nonmember/score'
      request({
        url: this.contextPath + url,
        method: 'get',
        params: this.form
      }).then(data => {
        data.forEach((d, i) => {
          this.$set(this.form.items, i, d);
        });
      });
      this.$refs.refReferrr.focus();
    },
    showResult () {

    },
    listToTextFormatter (list, val) {
      let data = list.find((value, index, arr) => {
        return value.code === val;
      });
      return !data ? '' : data['label'];
    }
  }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}
.handle-select {
    width: 280px;
}

.handle-input {
    width: 280px;
    display: inline-block;
}
.handle-select1 {
    width: 180px;
}

.handle-input1 {
    width: 180px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
.form-box {
    margin-left: 20px;
}
.form-box .title {
    text-align: center;
    margin-bottom: 15px;
}
</style>