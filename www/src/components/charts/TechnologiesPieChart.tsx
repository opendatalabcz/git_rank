import ReactApexChart from "react-apexcharts"
import {ITechnologyStatistics } from "../../types"

export default function TechnologiesPieChart({ technologies }: {technologies: ITechnologyStatistics[]}) {
          
    const series = technologies.map(technology => technology.total_changes)
    const options = {
      chart: {
        type: 'donut',
      },
      labels: technologies.map(technology => {
        switch(technology.technology){
          case "PYTHON":
            return ".py"
          case "JAVA":
            return ".java"
          default:
            return "other"
        }
      }),
      title: {
        text: 'File extension distribution'
      },
      responsive: [{
        breakpoint: 480,
        options: {
          legend: {
            position: 'bottom'
          },
        }
      }]
    }

    return (
      <div className="chart">
        <div>
            <ReactApexChart options={options} series={series} type="donut" height={"auto"} width={"100%"}/>
          </div>
        <div id="html-dist"></div>
      </div>
    );
  }