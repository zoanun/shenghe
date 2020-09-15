<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-setting"></i> 国标项目管理
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
        <el-select v-model="query.type"
                   placeholder="类别"
                   class="handle-select mr10"
        >
          <el-option key="A"
                     label="所有"
                     value="A"
          />
          <el-option v-for="item in combox.type"
                     :key="item.code"
                     :label="item.label"
                     :value="item.code"
          >
          </el-option>
        </el-select>
        <el-select v-model="query.nonmemberUseYn"
                   placeholder="非会员使用与否"
                   class="handle-select mr10"
        >
          <el-option key="A"
                     label="所有"
                     value="A"
          />
          <el-option v-for="item in combox.useYn"
                     :key="item.code"
                     :label="item.label"
                     :value="item.code"
          >
          </el-option>
        </el-select>
        <el-select v-model="query.memberUseYn"
                   placeholder="会员使用与否"
                   class="handle-select mr10"
        >
          <el-option key="A"
                     label="所有"
                     value="A"
          />
          <el-option v-for="item in combox.useYn"
                     :key="item.code"
                     :label="item.label"
                     :value="item.code"
          >
          </el-option>
        </el-select>
        <el-select v-model="query.useYn"
                   placeholder="检测项使用与否"
                   class="handle-select mr10"
        >
          <el-option key="A"
                     label="所有"
                     value="A"
          />
          <el-option v-for="item in combox.useYn"
                     :key="item.code"
                     :label="item.label"
                     :value="item.code"
          >
          </el-option>
        </el-select>
        <el-input v-model="query.name"
                  placeholder="项目名"
                  class="handle-input mr10"
        ></el-input>
        <el-button type="primary"
                   icon="el-icon-search"
                   @click="findClick"
        >
          搜索
        </el-button>
      </div>
      <!-- 表格 -->
      <el-table ref="itemTable"
                :data="tableData"
                border
                class="table"
                header-cell-class-name="table-header"
      >
        <el-table-column prop="id"
                         label="ID"
                         width="55"
                         align="center"
        ></el-table-column>
        <el-table-column label="类别"
                         width="100"
        >
          <template slot-scope="scope">
            <el-link type="primary"
                     @click="toggleType(scope.$index, scope.row)"
            >
              {{ listToTextFormatter(combox.type, scope.row.type) }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="name"
                         label="项目名"
        >
          <template slot-scope="scope">
            <el-input v-if="scope.row.isSelected"
                      v-model="scope.row.name"
                      v-focus
                      @focus="focusEvent(scope.row)"
                      @blur="blurEvent(scope.row)"
            ></el-input>
            <p v-else
               @click="cellClick(scope.row)"
            >
              {{ scope.row.name }}
            </p>
          </template>
        </el-table-column>
        <el-table-column label="非会员使用"
                         width="100"
        >
          <template slot-scope="scope">
            <el-link type="primary"
                     @click="toggleUseYn(scope.$index, scope.row, 'nonmemberUseYn')"
            >
              {{ listToTextFormatter(combox.useYn, scope.row.nonmemberUseYn) }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column label="会员使用"
                         width="100"
        >
          <template slot-scope="scope">
            <el-link type="primary"
                     @click="toggleUseYn(scope.$index, scope.row, 'memberUseYn')"
            >
              {{ listToTextFormatter(combox.useYn, scope.row.memberUseYn) }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column label="项目使用"
                         width="100"
        >
          <template slot-scope="scope">
            <el-link type="primary"
                     @click="toggleUseYn(scope.$index, scope.row, 'useYn')"
            >
              {{ listToTextFormatter(combox.useYn, scope.row.useYn) }}
            </el-link>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 编辑弹出框 -->
    <el-dialog :title="editDialog.title"
               :visible.sync="editDialog.editVisible"
               width="400px"
               @open="initDialog()"
    >
      <el-form ref="form"
               :model="form"
               :rules="rules"
               label-width="120px"
      >
        <el-form-item v-show="!editDialog.isAdd"
                      label="ID"
        >
          <el-input v-model="form.id"
                    :readonly="true"
                    class="handle-input"
          ></el-input>
        </el-form-item>
        <el-form-item label="类别">
          <el-select v-model="form.type"
                     placeholder="类别"
                     class="handle-select mr10"
          >
            <el-option v-for="item in combox.type"
                       :key="item.code"
                       :label="item.label"
                       :value="item.code"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目名"
                      prop="name"
        >
          <el-input ref="refItemName"
                    v-model="form.name"
                    class="handle-input"
                    @keyup.enter.native="saveAndContinue"
          ></el-input>
        </el-form-item>
        <el-form-item label="非会员使用与否">
          <el-select v-model="form.nonmemberUseYn"
                     placeholder="非会员使用与否"
                     class="handle-select mr10"
          >
            <el-option v-for="item in combox.useYn"
                       :key="item.code"
                       :label="item.label"
                       :value="item.code"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="会员使用与否">
          <el-select v-model="form.memberUseYn"
                     placeholder="会员使用与否"
                     class="handle-select mr10"
          >
            <el-option v-for="item in combox.useYn"
                       :key="item.code"
                       :label="item.label"
                       :value="item.code"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="项目使用与否">
          <el-select v-model="form.useYn"
                     placeholder="项目使用与否"
                     class="handle-select mr10"
          >
            <el-option v-for="item in combox.useYn"
                       :key="item.code"
                       :label="item.label"
                       :value="item.code"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer"
            class="dialog-footer"
      >
        <el-button @click="editDialog.editVisible = false; findClick();">关 闭</el-button>
        <el-button type="primary"
                   @click="saveAndContinue"
        >保存并继续</el-button>
        <el-button @click="saveClick">保 存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import request from '@/utils/request.js';
  export default {
    name: 'Nsim',
    data () {
      return {
        query: {
          type: '',
          nonmemberUseYn: '',
          memberUseYn: '',
          useYn: '',
          name: ''
        },
        combox: {
          useYn: [{
            code: 'Y',
            label: '使用'
          }, {
            code: 'N',
            label: '不使用'
          }],
          type: []
        },
        editDialog: {
          title: '',
          isAdd: false,
          editVisible: false,
        },
        rules: {
          name: [{ required: true, message: '请输入国标项目名字', trigger: 'blur' }],
        },
        tableData: [],
        viewStandardVisible: false,
        form: {},
        contextPath: localStorage.getItem('backendContextPath')
      };
    },
    mounted () {
      this.init();
    },
    methods: {
      init () {
        request({
          url: this.contextPath + '/bc/api/itemtype',
          method: 'get',
        }).then(result => {
          this.combox.type = result.map(data => {
            return { code: data[0], label: data[1] };
          });
          this.findClick();
        });
      },
      initDialog () {
        this.$nextTick(() => {
          this.$refs.refItemName.focus();
        });
      },
      addNew () {
        this.editDialog.title = '增加国标项目';
        this.editDialog.isAdd = true;
        this.editDialog.editVisible = true;
        this.form = {
          type: 1,
          nonmemberUseYn: 'Y',
          memberUseYn: 'Y',
          useYn: 'Y',
          name: ''
        };

      },
      findClick () {
        request({
          url: this.contextPath + '/bc/itemmaster',
          method: 'get',
          params: this.query
        }).then(data => {
          this.tableData = data.map(item => {
            return { ...item, isSelected: false };
          });
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
      },
      handleEdit (idx, row) {
        this.title = '修改国标项目';
        this.isAdd = false;
        this.editDialog.editVisible = true;
        this.form = row;
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
              this.form.name = '';
            });
          } else {
            this.$message.error('输入项有误，请检查！');
            return false;
          }
        });
      },
      doSave () {
        let url = '/bc/itemmaster/insert';
        return request({
          url: this.contextPath + url,
          method: 'post',
          data: this.form
        }).then(data => {
          this.$message.success('增加成功!');
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
      },
      toggleUseYn (idx, row, type) {
        let url = '/bc/itemmaster/update';
        row[type] = row[type] === 'Y' ? 'N' : 'Y';
        request({
          url: this.contextPath + url,
          method: 'post',
          data: row
        }).then(data => {
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
      },
      toggleType (idx, row) {
        let url = '/bc/itemmaster/update';
        row.type = row.type === 1 ? 2 : 1;
        request({
          url: this.contextPath + url,
          method: 'post',
          data: row
        }).then(data => {
        }).catch(e => {
          this.$message.error('发生错误，请联系管理员.');
        });
      },
      focusEvent (row) {
        row.oldName = row.name;
      },
      blurEvent (row) {
        row.isSelected = !row.isSelected;
        if (row.name !== row.oldName) {
          let url = '/bc/itemmaster/update';
          if (row.name === '') {
            this.$alert('不能输入空值', '警告', { type: 'error' });
            row.name = row.oldName;
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
      cellClick (row) {
        row.isSelected = !row.isSelected;
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