<template>
  <el-dialog :visible.sync="dialogVisible"
             :close-on-click-modal="false"
             :close-on-press-escape="false"
             title="体测报告"
             append-to-body
             width="800px"
             @opened="onOpened"
             @close="onClose"
  >
    <div>
      <div id="printMe" class="A4">
        <fieldset>
          <legend>盛和国际跆拳道少儿体测报告</legend>
          <div class="user">
            <el-form v-if="reportData && reportData.current_test && reportData.current_test.length > 0"
                     :inline="true"
            >
              <el-form-item label="用户">
                {{ name }}
              </el-form-item>
              <el-form-item label="年龄">
                {{ age }}
              </el-form-item>
              <el-form-item label="性别">
                {{ sex }}
              </el-form-item>
            </el-form>
          </div>
          <div class="chart">
          </div>
        </fieldset>
      </div>
      <div slot="footer">
        <el-button v-print="printProp"
                   type="primary"
        >
          打 印
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script>
  // import request from '@/utils/request.js';
  export default {
    name: 'BodyReport',
    components: {},
    props: {
      reportVisible: {
        type: Boolean,
        default: false
      },
      name: {
        type: String,
        default: ''
      },
      sex: {
        type: String,
        default: ''
      },
      age: {
        type: Number,
        default: 0
      },
      memberId: {
        type: String,
        default: ''
      },
      id: {
        type: Number,
        default: 0
      }
    },
    data () {
      return {
        dialogVisible: false,
        reportData: {},
        printProp: {
          id: 'printMe',
          popTitle: '盛和国际跆拳道'
        }
      };
    },
    watch: {
      reportVisible (val) {
        this.dialogVisible = val;
      }
    },
    methods: {
      onOpened () {/*
        request({
          url: this.contextPath + '/bc/report',
          method: 'get',
          params: {
            id: this.id,
            memberId: this.memberId
          }
        }).then(result => {
          console.log(result);
          this.reportData = result;
        });*/
      },
      onClose () {
        this.$emit('update:reportVisible', false);
      },

    }
  };
</script>

<style scoped>
@import '@/assets/css/pager.css';
@page {
    size: A4;
}

.line .item-title {
    font-size: 20px;
    font-weight: bold;
}
.line > div {
    display: inline-block;
    width: 100px;
}
.line .bar {
    height: 10px;
    border-radius: 10px;
}
.line .score {
    position: relative;
    left: -10px;
    top: 14px;
}
.line .name {
    position: relative;
    left: 40px;
}
.line .tag {
    position: relative;
    top: 8px;
    font-size: 1.5em;
}
.line .tag span {
    position: relative;
}
.line .desc .title {
    color: darkgreen;
    font-weight: bold;
    margin-bottom: 5px;
}
.line .desc span {
    font-size: 14px;
    line-height: 20px;
}
hr {
    margin-top: 10px;
    margin-bottom: 10px;
}
div >>> .el-dialog__header {
    background-color: #eeeeee;
    font-weight: bold;
}
.el-form-item {
    width: 200px;
}
div >>> .el-form-item__label {
    font-weight: bold;
}
#printMe {
    -webkit-print-color-adjust: exact;
}
</style>

