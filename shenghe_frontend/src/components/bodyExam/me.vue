<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-setting"></i> 会员录入
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-button icon="el-icon-circle-plus-outline"
                   class="mr10"
                   @click="addNew"
        >
          新增
        </el-button>
        <el-input v-model="query.memberId"
                  placeholder="会员编号"
                  class="handle-input1 mr10"
        ></el-input>
        <el-input v-model.number="query.age"
                  type="number"
                  placeholder="年龄"
                  class="handle-input1 mr10"
        >
        </el-input>
        <el-select v-model="query.sex"
                   placeholder="性别"
                   class="handle-select1 mr10"
        >
          <el-option key="A"
                     label="所有"
                     value="A"
          />
          <el-option v-for="item in combox.sex"
                     :key="item.code"
                     :label="item.label"
                     :value="item.code"
          >
          </el-option>
        </el-select>
        <el-input v-model="query.name"
                  placeholder="姓名"
                  class="handle-input1 mr10"
        >
        </el-input>
        <el-button type="primary"
                   icon="el-icon-search"
                   @click="findClick"
        >
          搜索
        </el-button>
      </div>
      <el-row>
        <el-col :span="10">
          <!-- 表格 -->
          <el-table ref="itemTable"
                    :data="tableData"
                    border
                    class="table"
                    header-cell-class-name="table-header"
                    @current-change="handleItemChange"
          >
            <el-table-column prop="id"
                             label="ID"
                             width="55"
                             align="center"
            >
            </el-table-column>
            <el-table-column prop="memberId"
                             label="会员编号"
                             width="100"
                             align="center"
            >
            </el-table-column>
            <el-table-column prop="age"
                             label="年龄"
                             width="80"
                             align="center"
            >
            </el-table-column>
            <el-table-column label="性别"
                             width="55"
            >
              <template slot-scope="scope">
                {{ listToTextFormatter(combox.sex, scope.row.sex) }}
              </template>
            </el-table-column>
            <el-table-column prop="name"
                             label="名字"
                             align="center"
            >
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button type="text"
                           icon="el-icon-delete"
                           @click="deleteMember(scope.$index, scope.row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
        <el-col :span="14">
          <div class="form-box">
            <div class="title">
              {{ form.title }}
            </div>
            <el-form ref="form"
                     :model="form"
                     :rules="rules"
                     label-width="180px"
            >
              <el-form-item label="会员编号">
                <el-input ref="refMemberId"
                          v-model="form.memberId"
                          placeholder="会员编号"
                          class="handle-input mr10"
                ></el-input>
              </el-form-item>
              <el-form-item label="姓名"
                            prop="name"
              >
                <el-input v-model="form.name"
                          placeholder="姓名"
                          class="handle-input mr10"
                ></el-input>
              </el-form-item>
              <el-form-item label="年龄"
                            prop="age"
              >
                <el-input v-model="form.age"
                          type="number"
                          :disabled="viewReport"
                          placeholder="年龄"
                          class="handle-input mr10"
                          @blur="initItem"
                ></el-input>
              </el-form-item>
              <el-form-item label="性别"
                            prop="sex"
              >
                <el-select v-model="form.sex"
                           :disabled="viewReport"
                           @change="initItem"
                >
                  <el-option v-for="item in combox.sex"
                             :key="item.code"
                             :label="item.label"
                             :value="item.code"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item v-for="(item) in form.items"
                            :key="item.id"
                            :label="item.name"
              >
                <el-input v-model="item.score"
                          :placeholder="item.name"
                          type="number"
                          class="handle-input mr10"
                ></el-input>
              </el-form-item>
            </el-form>
            <div style="text-align: center">
              <el-button @click="reset">
                重新填写
              </el-button>
              <el-button type="primary"
                         @click="saveClick"
              >
                保存
              </el-button>
              <el-button type="primary"
                         :disabled="!viewReport"
                         @click="showResult"
              >
                查看结果报表
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <BodyReport :report-data="reportData"
                :report-visible.sync="reportVisible"
                :name="form.name"
                :sex="listToTextFormatter(combox.sex, form.sex)"
                :age="form.age"
    >
    </BodyReport>
  </div>
</template>

<script>
  import request from '@/utils/request.js';
  import BodyReport from '@/components/bodyExam/BodyReport';
  export default {
    name: 'Nme',
    components: { BodyReport },
    data () {
      return {
        query: {
          memberId: '',
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
        reportData: [],
        reportVisible: false,
        viewReport: false,
        rules: {
          age: [
            { required: true, message: '请输入年龄', trigger: 'blur' }
          ],
          sex: [
            { required: true, message: '请输入性别', trigger: 'blur' }
          ]
        },
        contextPath: localStorage.getItem('backendContextPath')
      };
    },
    mounted () {
      this.init();
    },
    methods: {
      init () {
        this.findClick();
      },
      initItem () {
        if (this.form.age && this.form.sex) {
          return request({
            url: this.contextPath + '/bc/member/master',
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
        this.viewReport = false;
        this.$refs.refMemberId.focus();
      },
      findClick () {
        request({
          url: this.contextPath + '/bc/member',
          method: 'get',
          params: this.query
        }).then(data => {
          this.form = {
            items: []
          };
          this.tableData = data.map(item => {
            return { ...item, isSelected: false };
          });
          this.viewReport = false;
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
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
        let url = '/bc/member/insert';
        if (this.form.id === 0 || this.form.id) {
          url = '/bc/nonmember/update';
        }
        return request({
          url: this.contextPath + url,
          method: 'post',
          data: this.form
        }).then(data => {
          this.$message.success('操作成功!');
          this.findClick();
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
      },
      reset () {
        this.form.items = [];
        this.initItem();
        this.$refs.refMemberId.focus();
      },
      handleItemChange (row) {
        if (!row) {
          return;
        }
        let url = '/bc/member/score';
        request({
          url: this.contextPath + url,
          method: 'get',
          params: {
            id: row.id,
            memberId: row.memberId,
            age: row.age,
            sex: row.sex,
            name: row.name
          }
        }).then(data => {
          let items = [];
          data.forEach(d => {
            items.push(d);
          });
          this.form = {
            title: '查看信息',
            id: row.id,
            memberId: row.memberId,
            age: row.age,
            sex: row.sex,
            name: row.name,
            items: items
          };
        });
        this.viewReport = true;
        this.$refs.refMemberId.focus();
      },
      showResult () {
        let url = '/bc/member/update';
        return request({
          url: this.contextPath + url,
          method: 'post',
          data: this.form
        }).then(() => {

          url = '/bc/report';
          request({
            url: this.contextPath + url,
            method: 'post',
            data: this.form
          }).then(data => {
            this.reportData = data;
            this.reportVisible = true;
          });

        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
      },
      deleteMember (idx, row) {
        let url = '/bc/member/delete';
        return request({
          url: this.contextPath + url,
          method: 'post',
          data: { id: row.id }
        }).then(data => {
          this.$message.success('操作成功!');
          this.findClick();
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
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