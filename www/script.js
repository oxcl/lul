function add_info(box_id,name,value){
    let element = document.createElement("div");
    element.classList.add("info")
    let element_name = document.createElement("span");
    element_name.classList.add("name")
    element_name.innerText = name;
    let element_value = document.createElement("span")
    element_value.classList.add("value")
    element_value.innerText = value;
    element.appendChild(element_name)
    element.appendChild(element_value)
    document.querySelector(`#box-${box_id} .box-body`).appendChild(element)
}
(async ()=>{
    var result = await fetch("data.json")
    var data = await result.json();
    console.log(data)
    if(data.lul_is_on !== undefined){
        if(data.lul_is_on){
            document.querySelector(".header").classList.add("deactive")
        }
        else{
            document.querySelector(".header").classList.add("active")
        }
    }
    if(data.total_traffic_share !== undefined){
        add_info("ration","سهمیه موجود",data.total_traffic_share)
    }
    if(data.daily_traffic_share !== undefined){
        add_info("ration","سهمیه روزانه",Math.round(data.daily_traffic_share))
    }
    if(data.day_starts_at !== undefined){
        var now_hour = new Date().getHours()
        if(now_hour >= data.day_starts_at){
            add_info("allocation","سهمیه امروز اختصاص داده شده","بله")
        }
        else{
            add_info("allocation","سهمیه امروز اختصاص داده شده","نه")
        }
        add_info("allocation","زمان اختصاص سهمیه",`${data.day_starts_at}:00`)
    }

    const ctx = document.getElementById("canvas-remained").getContext('2d')

    result = await fetch("db/2023-8.csv")
    var csv = await result.text()
    console.log(csv)
    
    function csvToChartData(csv){
        const lines = csv.trim().split('\n')
        lines.shift()
        return lines.map(line =>{
            const [time, _, remained_traffic] = line.split(',');
            return {
                x: time * 1000,
                y: remained_traffic
            }
        })
    }

    const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Value',
            data: csvToChartData(csv),
            borderColor: '#3e95cd',
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                }
                // distribution: 'linear',
            },
            // title: {
            //     display: false,
            // }
        }
    }
    };
    new Chart(ctx,config)
})()


setTimeout(() => location.reload(),60000) // reload page every minute
