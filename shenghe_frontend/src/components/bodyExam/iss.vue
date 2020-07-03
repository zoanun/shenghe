<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-s-flag"></i> 项目打分标准
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <el-row>
        <el-col>
          <div class="handle-box">
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
              @click="findMasterItems">搜索</el-button>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
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
            <el-table-column prop="age"
              label="年龄"></el-table-column>
            <el-table-column label="性别">
              <template slot-scope="scope">
                {{ listToTextFormatter(combox.sex, scope.row.sex) }}
              </template>
            </el-table-column>
            <el-table-column prop="value"
              label="国标值"></el-table-column>
          </el-table>
        </el-col>
        <el-col :span="16">
          <!-- 右边内容 -->
          <el-card class="box-card"
            shadow="never">
            <div slot="header"
              class="clearfix">
              <span>{{ currentMasterItem ? currentMasterItem.name : '' }} - {{ listToTextFormatter(combox.sex, currentMasterItem.sex) }} - {{ currentMasterItem.age }} 岁</span>
              <el-button style="float: right; padding: 3px 0"
                type="text"
                @click="saveClick">保存</el-button>
            </div>
            <div>
              <el-form ref="form"
                label-width="180px"
                :inline="true">
                <div v-for="type in combox.periodType"
                  :key="type.code">
                  <el-row>
                    <el-col>
                      <el-form-item :label="type.label + '评价最低'">
                        <el-input v-model="form.data[type.code+'_lowScore']"
                          type="number"
                          :placeholder="type.label + '评价最低'"
                          class="handle-input"></el-input>
                      </el-form-item>
                      <el-form-item :label="type.label + '评价最高'">
                        <el-input v-model="form.data[type.code+'_highScore']"
                          type="number"
                          :placeholder="type.label + '评价最高'"
                          class="handle-input"></el-input>
                      </el-form-item>
                      <el-form-item :label="type.label + '展示颜色'">
                        <el-color-picker v-model="form.data[type.code+'_color']"></el-color-picker>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col>
                      <el-form-item :label="type.label + '评价的评语'">
                        <el-input v-model="form.data[type.code+'_scoreDesc']"
                          :placeholder="type.label + '评价的评语'"
                          class="ta"
                          type="textarea"
                          :rows="5"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-row>

                </div>
              </el-form>
              <el-row>
                <el-col style="text-align:center">
                  <el-button @click="saveClick"
                    type="primary">保存</el-button>
                </el-col>
              </el-row>
            </div>
          </el-card>
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
        age: '',
        sex: ''
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
        periodType: [],
        sex: [{
          code: 'M',
          label: '男性'
        }, {
          code: 'F',
          label: '女性'
        }],
      },
      masterData: [],
      form: {        itemId: null, data: {
          SUPERLOWER_lowScore: 0,
          SUPERLOWER_highScore: 0,
          SUPERLOWER_scoreDesc: '',
          SUPERLOWER_color: '#FF00FF',
          LOWER_lowScore: 0,
          LOWER_highScore: 0,
          LOWER_scoreDesc: '',
          LOWER_color: '#FF00FF',
          NORMAL_lowScore: 0,
          NORMAL_highScore: 0,
          NORMAL_scoreDesc: '',
          NORMAL_color: '#FF00FF',
          HIGH_lowScore: 0,
          HIGH_highScore: 0,
          HIGH_scoreDesc: '',
          HIGH_color: '#FF00FF',
          SUPERHIGH_lowScore: 0,
          SUPERHIGH_highScore: 0,
          SUPERHIGH_scoreDesc: '',
          SUPERHIGH_color: '#FF00FF',
        }
      },
      currentMasterItem: { type: '', name: '' },
      contextPath: localStorage.getItem('backendContextPath')
    };
  },
  mounted () {
    this.init();
  },
  methods: {
    init () {
      this.initCombox();
      this.findPeriodType().then(() => {
        this.findMasterItems();
      });
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
    findMasterItems () {
      return request({
        url: this.contextPath + '/bc/scorestandard/master',
        method: 'get',
        params: this.query
      }).then(data => {
        this.masterData = data;
        this.$nextTick(() => {
          if (this.masterData.length > 0) {
            if (this.currentMasterItem) {
              let row = this.masterData.find(data => {
                return data.id === this.currentMasterItem.id;
              });
              if (row) {
                this.$refs.refMasterTable.setCurrentRow(row);
              }
            } else {
              this.$refs.refMasterTable.setCurrentRow(this.masterData[0]);
              this.currentMasterItem = this.masterData[0];
            }
          }
        });

      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      })
    },
    findPeriodType () {
      return request({
        url: this.contextPath + '/bc/api/periodtype',
        method: 'get',
      }).then(result => {
        this.combox.periodType = result.map(data => {
          return { code: data[0], label: data[1] };
        });
      });
    },
    findScoreStandard (id) {
      request({
        url: this.contextPath + '/bc/scorestandard',
        method: 'get',
        params: { itemDetailId: id }
      }).then(data => {
        let oldForm = this.form;
        this.form = {          itemId: id, data: {
            SUPERLOWER_lowScore: 0,
            SUPERLOWER_highScore: 0,
            SUPERLOWER_scoreDesc: '',
            SUPERLOWER_color: '#FF00FF',
            LOWER_lowScore: 0,
            LOWER_highScore: 0,
            LOWER_scoreDesc: '',
            LOWER_color: '#FF00FF',
            NORMAL_lowScore: 0,
            NORMAL_highScore: 0,
            NORMAL_scoreDesc: '',
            NORMAL_color: '#FF00FF',
            HIGH_lowScore: 0,
            HIGH_highScore: 0,
            HIGH_scoreDesc: '',
            HIGH_color: '#FF00FF',
            SUPERHIGH_lowScore: 0,
            SUPERHIGH_highScore: 0,
            SUPERHIGH_scoreDesc: '',
            SUPERHIGH_color: '#FF00FF',
          }        };
        if (data.length === 0) {
          this.combox.periodType.forEach(type => {
            this.form.data[type.code + "_lowScore"] = this.currentMasterItem.value;
            this.form.data[type.code + "_highScore"] = this.currentMasterItem.value;
            this.form.data[type.code + "_scoreDesc"] = '';
            if (oldForm && oldForm.data && oldForm.data[type.code + "_color"]) {
              this.form.data[type.code + "_color"] = oldForm.data[type.code + "_color"];
            } else {
              this.form.data[type.code + "_color"] = "#FFFFFF";
            }
          });
        } else {
          data.forEach(d => {
            this.form.data[d.periodType + "_lowScore"] = d.lowScore;
            this.form.data[d.periodType + "_highScore"] = d.highScore;
            this.form.data[d.periodType + "_scoreDesc"] = d.scoreDesc;
            this.form.data[d.periodType + "_color"] = d.color;
          })
        }
      }).catch(e => {
        this.$message.error('发生错误，请联系管理员.');
      });
    },
    handleItemChange (row) {
      this.currentMasterItem = row;
      if (row) {
        this.findScoreStandard(row.id);
      }

    },
    saveClick () {
      this.form.itemDetailId = this.currentMasterItem.id;
      let url = '/bc/scorestandard/insert';
      return request({
        url: this.contextPath + url,
        method: 'post',
        data: this.form
      }).then(data => {
        this.$message.success('保存成功!');
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
.box-card {
    margin-left: 10px;
}
.mr10 {
    margin-right: 10px;
}
.ta {
    width: 600px;
}
</style>