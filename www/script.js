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
    const today = new Date()
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
    add_info("ration","سهمیه موجود",Math.round(data.total_traffic_share))
    add_info("ration","سهمیه روزانه",Math.round(data.daily_traffic_share))
    add_info("allocation","سهمیه امروز اختصاص داده شده",(today.getHours() >= data.day_starts_at ) ? "بله" : "نه")
    add_info("allocation","زمان اختصاص سهمیه",`${data.day_starts_at}:00`)

    // draw graphs
    const csv_file = `db/${today.getFullYear()}-${today.getMonth()+1}.csv`
    const jalali_csv_file = `db/jalali/${today_in_jalali.jy}-${today_in_jalali.jm}.csv`
    const database = await fetch_csv(csv_file)
    const jalali_database = await fetch_csv(jalali_csv_file)

    Chart.defaults.font.family = 'Calibri, "Helvetica Neue", Helvetica, Arial, sans-serif'
    Chart.defaults.font.size = (window.innerWidth >= 800) ? 16 : 12 //(window.innerWidth)

    const ctx1 = create_graph('remained','نمودار حجم باقی مانده')
    const gradient_off = ctx1.createLinearGradient(0, 0, 0, 400);
    gradient_off.addColorStop(0,COLORS.total_gradient_lul_off0);   
    gradient_off.addColorStop(1,COLORS.total_gradient_lul_off1);
    const gradient_on = ctx1.createLinearGradient(0, 0, 0, 400);
    gradient_on.addColorStop(0,COLORS.total_gradient_lul_on0);   
    gradient_on.addColorStop(1,COLORS.total_gradient_lul_on1);
    const get_datasets = {
        remained: function get_datasets_for_remained_graph(database){
            return [
                {
                    label: 'ترافیک باقی مانده',
                    data: get_data_from_database(database,"remained_traffic"),
                    borderColor: COLORS.default,
                },
                {
                    label: 'کل ترافیک',
                    data: get_data_from_database(database,"total_traffic"),
                    borderColor: COLORS.total_lul_off,
                    fill: {target: 'origin',above: (data.lul_is_on ? gradient_on : gradient_off)}
                },
                {
                    label: 'حد مصرف مجاز',
                    data: get_data_from_database(database,"required_traffic_in_reserve"),
                    borderColor: COLORS.required_traffic_in_reserve,
                }
            ]
        },
        usage: function get_datasets_for_usage_graph(database){
            return [{
                label: 'ترافیک مصرف شده',
                data: get_data_from_database(database,"usage"),
                borderColor: COLORS.default,
            }]
        }
    }
    const graphs = {}
    graphs.remained = draw_graph(ctx1,get_datasets.remained(database),timespans.day)
    const ctx2 = create_graph('usage','نمودار مصرف')
    graphs.usage = draw_graph(ctx2,get_datasets.usage(database),timespans.day)

    document.querySelectorAll('select').forEach((element) => {
        element.addEventListener('change',(event)=>{
            const timespan = event.target.value
            const graph_name = event.target.getAttribute('data-graph-name')
            graphs[graph_name].options.scales.x.min = timespans[timespan].min
            graphs[graph_name].options.scales.x.max = timespans[timespan].max
            graphs[graph_name].options.scales.x.time.unit = timespans[timespan].time.unit
            if(timespan === 'jmonth'){
                graphs[graph_name].data.datasets = get_datasets[graph_name](jalali_database)
                graphs[graph_name].options.scales.x.adapters.date.locale = 'fa-IR'
            }
            else{
                graphs[graph_name].data.datasets = get_datasets[graph_name](database)
                graphs[graph_name].options.scales.x.adapters.date.locale = 'en-US'
            }
            graphs[graph_name].update()
        })
    })

})()

setTimeout(() => location.reload(),600000) // reload page every 10 minutes