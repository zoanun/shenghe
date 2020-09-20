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
      <div id="printMe">
        <div id="user">
          <span id="user-name"> {{ name }} </span>
          <span id="user-age"> {{ age }} </span>
          <span id="user-sex"> {{ sex }} </span>
        </div>
        <div id="health">
          <p>身高：{{ height }}</p>
          <p>体重：{{ weight }}</p>
        </div>
        <div id="ability">
          <table id="ability-current" class="gridtable">
            <caption>本次测试 (<span v-show="reportData.currentTestDate">{{ reportData.currentTestDate }}</span>) </caption>
            <tbody v-if="reportData.currentTest.length > 0">
              <tr v-for="data in reportData.currentTest.filter(d=>d.type===2)" :key="data.name">
                <th>{{ data.name }}</th>
                <td>{{ data.score + data.unit }}</td>
                <td>{{ data.periodName }}</td>
              </tr>
            </tbody>
          </table>
          <table id="ability-latest" class="gridtable">
            <caption>上次测试 (<span v-show="reportData.latestTestDate">{{ reportData.latestTestDate }}</span>) </caption>
            <tbody v-if="reportData.latestTest.length > 0">
              <tr v-for="data in reportData.latestTest.filter(d=>d.type===2)" :key="data.name">
                <th>{{ data.name }}</th>
                <td>{{ data.score + data.unit }}</td>
                <td>{{ data.periodName }}</td>
              </tr>
            </tbody>
            <tbody v-if="reportData.latestTest.length === 0 && reportData.currentTest.length > 0">
              <tr v-for="data in reportData.currentTest.filter(d=>d.type===2)" :key="data.name">
                <th>{{ data.name }}</th>
                <td>  </td>
                <td>  </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div id="chart">
          <div id="chart-radar" ref="refRadar"></div>
          <div id="chart-line">
            <img src="@/assets/img/legend.png" class="legend">
            <el-form label-width="130px">
              <el-form-item v-for="item in reportData.currentTest.filter(d=>d.type === 2)"
                            :key="item.id"
                            :label="item.name + '(' + item.score + ')'"
              >
                <div v-for="(level) in item.level"
                     :key="level.periodType + 'tag'"
                     class="tag"
                >
                  <span v-if="level.inLevel === 'Y'"
                        :style="{position: 'relative', left: Math.abs(item.displayScore - level.lowScore) / Math.abs(level.highScore - level.lowScore) * 25 + 'px'}"
                  ><img src="@/assets/img/tag.png">
                  </span>
                </div>
                <br />
                <div v-for="level in item.level"
                     :key="level.periodType + 'bar'"
                     class="bar"
                     :style="{'background-color': level.color}"
                >
                </div>
              </el-form-item>
            </el-form>
          </div>
          <div id="descript">
            {{ reportData.currentTestDesc }}
          </div>
        </div>
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
  import request from '@/utils/request.js';
  import echarts from 'echarts';
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
        reportData: { currentTest: [], latestTest: [], currentTestDesc: '' },
        contextPath: localStorage.getItem('backendContextPath'),
        height: '',
        weight: '',
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
      onOpened () {
        request({
          url: this.contextPath + '/bc/report',
          method: 'post',
          data: {
            id: this.id,
            memberId: this.memberId
          }
        }).then(result => {
          console.log(result);
          this.reportData = result;
          this.height = result.currentTest.find(test=>test.name === '身高').score + ' cm';
          this.weight = result.currentTest.find(test=>test.name === '体重').score + ' kg';
          this.drawCharts();
        });
      },
      onClose () {
        this.$emit('update:reportVisible', false);
      },
      drawCharts() {
        // let radar = echarts.init(this.$refs.refRadar);
        let radar = echarts.init(document.getElementById('chart-radar'));
        let showData = this.reportData.currentTest.filter(test=>test.type === 2);
        let indicator = showData.map(test=>{
          return { name: test.name , max: 4 };
        });
        let data = showData.map(test=>{
          return test.periodScore;
        });
        radar.setOption({
          tooltip: {},
          legend: {
            data: []
          },
          radar: {
            nameGap: 10,
            radius: 75,
            name: {
              textStyle: {
                color: '#000',
                textDecoration: 'underline',
                // backgroundColor: '#f7f886',
                borderRadius: 3,
                padding: [3, 5]
              }
            },
            shape: 'circle',
            indicator: indicator
          },
          series: [{
            type: 'radar',
            name: '',
            data: [
              {
                areaStyle: {
                  normal: {
                    color: 'rgba(255,0,0,0.6)'
                  }
                },
                value: data
              },
            ]
          }]
        });
      }
    }
  };
</script>

<style scoped>
#printMe {
    width: 756px;
    height: 1086px;
    background-image: url(../../assets/img/report-bg.png);
    -webkit-print-color-adjust: exact;
}
#user {
    position: relative;
    top: 125px;
    left: 200px;
    font-weight: bold;
    font-family: SimHei;
    font-size: 1.5em;
    color: #fefefe;
}
#user-name {
    position: relative;
}
#user-age {
    position: relative;
    left: 120px;
}
#user-sex {
    position: relative;
    left: 260px;
}
#health {
    position: relative;
    top: 390px;
    left: 110px;
}
#health p {
    font-weight: bold;
    font-family: SimHei;
    font-size: 1.2em;
    color: #fefefe;
    margin-left: 10px;
    margin-bottom: 5px;
}
caption {
    margin-bottom: 5px;
}
table.gridtable {
    font-family: verdana, arial, sans-serif;
    font-size: 0.5em;
    color: #333333;
    border-width: 1px;
    border-color: #666666;
    border-collapse: collapse;
}
table.gridtable th {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #fefefe;
    background-color: #b51d40;
    color: #fefefe;
}

table.gridtable td {
    border-width: 1px;
    padding: 8px;
    min-width: 30px;
    border-style: solid;
    border-color: #b51d40;
    background-color: #ffffff;
}
table.gridtable td:last-child {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #b51d40;
    background-color: #f5e3e1;
}
#ability {
    position: relative;
    top: 135px;
    left: 270px;
    font-weight: bold;
    font-family: SimHei;
    font-size: 1.5em;
    color: #fefefe;
}
#ability-current {
    position: relative;
    height: 250px;
    margin-right: 10px;
    float: left;
}
#ability-latest {
    position: relative;
    top: 0;
    float: left;
    height: 250px;
}

#chart {
    position: relative;
    top: 220px;
    left: 450px;
    float: left;
}
#chart-radar {
    position: relative;
    left: -390px;
    top: 0px;
    text-align: left;
    width: 290px;
    height: 290px;
    float: left;
    z-index: 110;
}
#chart-line {
    position: relative;
    left: -370px;
    top: 10px;
    width: 300px;
    text-align: left;
    float: left;
    z-index: 100;
}
#chart-line >>> .el-form-item__content {
    margin-left: 0px !important;
    line-height: 12px;
}
#chart-line >>> div {
    display: inline-block;
}
#chart-line .bar {
    height: 10px;
    width: 35px;
    border-radius: 10px;
}
#chart-line .score {
    position: relative;
    left: -10px;
    top: 14px;
}
#chart-line .name {
    position: relative;
    left: 40px;
}
#chart-line >>> .tag {
    position: relative;
    font-size: 1.5em;
    width: 35px;
}

#chart-line >>> .el-form-item {
    margin-bottom: 5px;
}

#descript {
    position: relative;
    top: 80px;
    left: -350px;
    width: 570px;
    float: left;
}

.legend {
    position: relative;
    left: 120px;
    margin-bottom: 5px;
}
/*去除页眉页脚*/
@page {
    size: auto; /* auto is the initial value */
    margin: 3mm; /* this affects the margin in the printer settings */
}

html {
    background-color: #ffffff;
    margin: 0; /* this affects the margin on the html before sending to printer */
}

body {
    border: solid 1px blue;
    margin: 10mm 15mm 10mm 15mm; /* margin you want for the content */
}
/*去除页眉页脚*/
</style>

