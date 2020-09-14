<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-box"></i> 国标数据录入
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <el-row>
        <el-col :span="6">
          <!-- 左边表格 -->
          <el-table :data="masterData"
            ref="refMasterTable"
            border
            class="table"
            header-cell-class-name="table-header"
            highlight-current-row
            @current-change="handleItemChange">
            <el-table-column prop="id"
              label="ID"
              width="55"></el-table-column>
            <el-table-column label="类别"
              width="100">
              <template slot-scope="scope">
                {{ listToTextFormatter(combox.type, scope.row.type) }}
              </template>
            </el-table-column>
            <el-table-column prop="name"
              label="项目名"></el-table-column>
            <el-table-column prop="cnt"
              label="已设置个数"></el-table-column>
          </el-table>
        </el-col>
        <el-col :span="18">
          <div class="handle-box">
            <el-button icon="el-icon-circle-plus-outline"
              class="mr10"
              @click="addNew"
              :disabled="!currentMasterItem.id">新增</el-button>
            <el-input v-model="query.age"
              placeholder="年龄"
              type="number"
              class="handle-input mr10"></el-input>
            <el-select v-model="query.sex"
              placeholder="性别"
              class="handle-select mr10">
              <el-option key="A"
                label="所有"
                value="A" />
              <el-option v-for="item in combox.sex"
                :key="item.code"
                :label="item.label"
                :value="item.code">
              </el-option>
            </el-select>
            <el-button type="primary"
              icon="el-icon-search"
              @click="findClick">搜索</el-button>
          </div>
          <!-- 右边表格 -->
          <el-table :data="detailData"
            border
            class="table tm"
            header-cell-class-name="table-header"
            highlight-current-row>
            <el-table-column prop="id"
              label="ID"
              width="55"></el-table-column>
            <el-table-column prop="item.name"
              label="项目"></el-table-column>
            <el-table-column prop="staDate"
              label="开始日期">
              <template slot-scope="scope">
                <el-date-picker v-if="scope.row.f_staDate.isSelected"
                  @focus="focusEvent(scope.row, 'f_staDate')"
                  @blur="blurEvent(scope.row, 'f_staDate')"
                  v-focus
                  v-model="scope.row.staDate"
                  type="date"
                  :picker-options="startDatePicker(scope.row.endDate)"
                  format="yyyy-MM-dd"
                  value-format="yyyy-MM-dd"
                  placeholder="开始日期">
                </el-date-picker>
                <p @click="cellClick(scope.row, 'f_staDate')"
                  v-else>{{scope.row.staDate}}</p>
              </template>
            </el-table-column>
            <el-table-column prop="endDate"
              label="结束日期">
              <template slot-scope="scope">
                <el-date-picker v-if="scope.row.f_endDate.isSelected"
                  @focus="focusEvent(scope.row, 'f_endDate')"
                  @blur="blurEvent(scope.row, 'f_endDate')"
                  v-model="scope.row.endDate"
                  type="date"
                  :picker-options="endDatePicker(scope.row.staDate)"
                  format="yyyy-MM-dd"
                  value-format="yyyy-MM-dd"
                  default-value="2999-12-31"
                  placeholder="结束日期">
                </el-date-picker>
                <p @click="cellClick(scope.row, 'f_endDate')"
                  v-else>{{scope.row.endDate}}</p>
              </template>
            </el-table-column>
            <el-table-column prop="age"
              label="年龄">
              <template slot-scope="scope">
                <el-input v-if="scope.row.f_age.isSelected"
                  v-model="scope.row.age"
                  type="number"
                  @focus="focusEvent(scope.row, 'f_age')"
                  @blur="blurEvent(scope.row, 'f_age')"
                  v-focus></el-input>
                <p @click="cellClick(scope.row, 'f_age')"
                  v-else>{{scope.row.age}}</p>
              </template>
            </el-table-column>
            <el-table-column label="性别">
              <template slot-scope="scope">
                <el-link type="primary"
                  @click="toggleSex(scope.$index, scope.row)">{{ listToTextFormatter(combox.sex, scope.row.sex) }}</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="value"
              label="标准值">
              <template slot-scope="scope">
                <el-input v-if="scope.row.f_value.isSelected"
                  v-model="scope.row.value"
                  @focus="focusEvent(scope.row, 'f_value')"
                  @blur="blurEvent(scope.row, 'f_value')"
                  v-focus></el-input>
                <p @click="cellClick(scope.row, 'f_value')"
                  v-else>{{scope.row.value}}</p>
              </template>
            </el-table-column>
            <el-table-column label="操作"
              width="300">
              <template slot-scope="scope">
                <el-button type="text"
                  icon="el-icon-delete"
                  @click="deleteDetail(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <!-- 右边表单 -->
          <el-dialog :title="editDialog.title"
            :visible.sync="editDialog.editVisible"
            width="500px"
            @open="initDialog()">
            <div class="form-box">
              <el-form ref="form"
                :rules="rules"
                :model="form"
                label-width="80px">
                <el-form-item label="类别">
                  <el-select v-model="currentMasterItem.type"
                    disabled>
                    <el-option v-for="item in combox.type"
                      :key="item.code"
                      :label="item.label"
                      :value="item.code">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="项目"
                  prop="name">
                  <el-input v-model="currentMasterItem.name"
                    :readonly="true"
                    class="handle-input"></el-input>
                </el-form-item>
                <el-form-item label="年龄"
                  prop="age">
                  <el-input v-model.trim="form.age"
                    type="number"
                    ref="refFormAge"
                    @keyup.enter.native="saveAndContinue"
                    class="handle-input"></el-input>
                </el-form-item>
                <el-form-item label="性别"
                  prop="sex">
                  <el-select v-model="form.sex">
                    <el-option v-for="item in combox.sex"
                      :key="item.code"
                      :label="item.label"
                      :value="item.code">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="开始日期"
                  prop="staDate">
                  <el-date-picker v-model="form.staDate"
                    type="date"
                    :picker-options="startDatePicker(form.endDate)"
                    format="yyyy-MM-dd"
                    default-value=""
                    value-format="yyyy-MM-dd"
                    placeholder="开始日期">
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="结束日期"
                  prop="endDate">
                  <el-date-picker v-model="form.endDate"
                    type="date"
                    :picker-options="endDatePicker(form.staDate)"
                    format="yyyy-MM-dd"
                    value-format="yyyy-MM-dd"
                    default-value="2999-12-31"
                    placeholder="结束日期">
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="标准值"
                  prop="value">
                  <el-input v-model.trim="form.value"
                    ref="refFormValue"
                    oninput="value=value.replace(/[^0-9.]/g, '')"
                    class="handle-input"
                    @keyup.enter.native="saveAndContinue"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer"
                class="dialog-footer">
                <el-button @click="editDialog.editVisible = false;findDetailItems(currentMasterItem.id)">关 闭</el-button>
                <el-button type="primary"
                  @click="saveAndContinue">保存并继续</el-button>
                <el-button @click="saveClick">保 存</el-button>
              </span>
            </div>
          </el-dialog>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request.js';
export default {
  name: 'nsde',
  data () {
    return {
      query: {
        age: '',
        sex: '',
      },
      combox: {
        useYn: [{
          code: 'Y',
          label: '使用'
        }, {
          code: 'N',
          label: '不使用'
        }],
        type: [],
        sex: [{
          code: 'M',
          label: '男性'
        }, {
          code: 'F',
          label: '女性'
        }],
      },
      masterData: [],
      detailData: [],
      form: {
        endDate: '2999-12-31'
      },
      rules: {
        age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
        sex: [{ required: true, message: '请输入性别', trigger: 'blur' }],
        staDate: [{ required: true, message: '请输入开始日期', trigger: 'blur' }],
        endDate: [{ required: true, message: '请输入结束日期', trigger: 'blur' }],
        value: [{ required: true, message: '请输入标准值', trigger: 'blur' }],
      },
      currentMasterItem: { type: '', name: '' },
      editDialog: {
        title: '',
        editVisible: false,
      },
      contextPath: localStorage.getItem('backendContextPath')
    };
  },
  mounted () {
    this.init();
  },
  methods: {
    init () {
      this.initCombox();
      this.findMasterItems();
    },
    initCombox () {
      request({
        url: this.contextPath + '/bc/api/itemtype',
        method: 'get',
      }).then(result => {
        this.combox.type = result.map(data => {
          return { code: data[0], label: data[1] };
        });
      });
    },
    initDialog () {

    },
    findMasterItems () {
      request({
        url: this.contextPath + '/bc/itemdetail/master',
        method: 'get',
      }).then(data => {
        this.masterData = data;
        if (this.masterData.length > 0) {
          if (this.currentMasterItem.id) {
            let row = this.masterData.find(data => {
              return data.id === this.currentMasterItem.id;
            });
            if (row) {
              this.$refs.refMasterTable.setCurrentRow(row);
            }
          } else {
            this.currentMasterItem = this.masterData[0];
            this.$refs.refMasterTable.setCurrentRow(this.masterData[0]);
          }
        }
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      })
    },
    findDetailItems (id) {
      this.query.itemId = id;
      request({
        url: this.contextPath + '/bc/itemdetail',
        method: 'get',
        params: this.query
      }).then(data => {
        this.detailData = data.map(item => {
          return {            ...item,
            f_age: { isSelected: false },
            f_sex: { isSelected: false },
            f_staDate: { isSelected: false },
            f_endDate: { isSelected: false },
            f_value: { isSelected: false },
            old: {}
          };
        });
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      });
    },
    addNew () {
      if (this.currentMasterItem.id) {
        this.editDialog.editVisible = true;
      }
    },
    findClick () {
      if (this.currentMasterItem.id) {
        this.findDetailItems(this.currentMasterItem.id);
      }
    },
    startDatePicker (endDate) {
      return {
        disabledDate (time) {
          if (endDate) {  //如果结束时间不为空，则小于结束时间
            return new Date(endDate).getTime() < time.getTime()
          } else {
            // return time.getTime() > Date.now()//开始时间不选时，结束时间最大值小于等于当天
          }
        }
      }
    },
    endDatePicker (staDate) {
      return {
        disabledDate (time) {
          if (staDate) {  //如果结束时间不为空，则小于结束时间
            return new Date(staDate).getTime() > time.getTime()
          } else {
            // return time.getTime() > Date.now()//开始时间不选时，结束时间最大值小于等于当天
          }
        }
      }
    },
    handleItemChange (row) {
      this.query.age = '';
      this.query.sex = '';
      this.currentMasterItem = row;
      this.findDetailItems(row.id)
    },
    saveClick () {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.doSave().then(() => {
            this.editDialog.editVisible = false;
          });
        } else {
          this.$message.error('输入项有误，请检查！');
          return false;
        }
      });
    },
    saveAndContinue () {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.doSave().then(() => {
            this.form.value = '0';
            this.form.sex = this.form.sex == 'M' ? 'F' : 'M';
            this.$refs.refFormAge.focus();
            this.findMasterItems();
          });
        } else {
          this.$message.error('输入项有误，请检查！');
          return false;
        }
      });
    },
    doSave () {
      this.form.itemId = this.currentMasterItem.id;
      let url = '/bc/itemdetail/insert';
      return request({
        url: this.contextPath + url,
        method: 'post',
        data: this.form
      }).then(data => {
        this.$message.success('增加成功!');
        this.findMasterItems();
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      });
    },
    deleteDetail (idx, row) {
      let url = '/bc/itemdetail/delete';
      return request({
        url: this.contextPath + url,
        method: 'post',
        data: row
      }).then(data => {
        this.$message.success('删除成功!');
        this.findMasterItems();
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      });
    },
    updateDetail (idx, row) {
      let url = '/bc/itemdetail/update';
      return request({
        url: this.contextPath + url,
        method: 'post',
        data: row
      }).then(data => {
        this.$message.success('修改成功!');
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      });
    },
    focusEvent (row, type) {
      row.old[type] = row[type.substring(2)]
    },
    blurEvent (row, type) {
      row[type].isSelected = !row[type].isSelected
      if (row[type.substring(2)] !== row.old[type]) {
        let url = '/bc/itemdetail/update';
        if (row[type.substring(2)] === '') {
          this.$alert('不能输入空值', '警告', { type: 'error' });
          row.name = row.old[type];
          return;
        }
        request({
          url: this.contextPath + url,
          method: 'post',
          data: row
        }).then(data => {
          this.$message.success('操作成功!');
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
      }
    },
    cellClick (row, type) {
      row[type].isSelected = !row[type].isSelected
    },
    toggleSex (idx, row) {
      row.sex = row.sex === 'F' ? 'M' : 'F';
      this.updateDetail(idx, row);
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
    margin-left: 10px;
}

.handle-select {
    width: 180px;
}

.handle-input {
    width: 180px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.tm {
    margin-left: 10px;
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
</style>