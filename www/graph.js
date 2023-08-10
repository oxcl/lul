const today = new Date()
const today_in_jalali = jalaali.toJalaali(today)
const timespans = {
    day: {
        min: new Date(today.getFullYear(),today.getMonth(),today.getDate(),0,0,0).getTime(),
        max: new Date(today.getFullYear(),today.getMonth(),today.getDate() + 1,0,0,0).getTime(),
        time: { unit: 'hour'}
    },
    yesterday: {
        min: new Date(today.getFullYear(),today.getMonth(),today.getDate() - 1,0,0,0).getTime(),
        max: new Date(today.getFullYear(),today.getMonth(),today.getDate(),0,0,0).getTime(),
        time: { unit: 'hour'}
    },
    month: {
        min: new Date(today.getFullYear(),today.getMonth(),1,0,0,0).getTime(),
        max: new Date(today.getFullYear(),today.getMonth()+1,0,0,0,0).getTime(),
        time: { unit: 'day'}
    },
    jmonth: {
        min: jalaali.jalaaliToDateObject(today_in_jalali.jy,today_in_jalali.jm,1).getTime(),
        max: jalaali.jalaaliToDateObject(today_in_jalali.jy,today_in_jalali.jm + 1,0).getTime(),
        time: { unit: 'day'}
    }
}
const COLORS = {
    default: 'rgba(41, 128, 185,1.0)',
    total_lul_off: 'rgba(39, 174, 96,1)',
    total_gradient_lul_off0: 'rgba(39, 174, 96,.5)',
    total_gradient_lul_off1: 'rgba(39, 174, 96,0)',
    total_lul_on: 'rgba(192, 57, 43,1.0)',
    total_gradient_lul_on0: 'rgba(192, 57, 43,.5)',
    total_gradient_lul_on1: 'rgba(192, 57, 43,0)',
    required_traffic_in_reserve: 'rgba(127, 140, 141,1.0)',
}
// fetch csv file and parse it into a map with csv titles as keys and an array of data as values
async function fetch_csv(csv_file_to_fetch){
    const result = await fetch(csv_file_to_fetch)
    const csv = await result.text()
    const lines = csv.trim().split('\n')
    const map = new Map()
    const titles = lines.shift().split(',')
    for(const title of titles){ // remove csv titles line
        map.set(title,[])
    }
    for(const line of lines){
        const line_arr = line.split(',')
        let i = 0
        for(const key of map.keys()){
            map.get(key).push(Number.parseInt(line_arr[i]))
            i++;
        }
    }
    return map
}
function get_data_from_database(database,item){
    return database.get(item).map((value,index)=>{
        return {
            x: database.get('time')[index],
            y: value
        }
    })
}
function create_graph(name,title){
    const element = document.createElement('div')
    element.classList.add('box','graph')
    element.id = `box-graph-${name}`
    element.innerHTML = `
        <div class="box-header">
            ${title}
            <select class="timespan-selector" id="timespan-selector-${name}" data-graph-name="${name}">
                <option value="day">امروز</option>
                <option value="yesterday">دیروز</option>
                <option value="jmonth">این ماه (شمسی)</option>
                <option value="month">این ماه (میلادی)</option>
            </select>
        </div>
        <div class="box-body">
            <canvas id="canvas-${name}"></canvas>
        </div>
    `
    document.querySelector('.container').appendChild(element)
    return element.querySelector('canvas').getContext('2d')
}
function draw_graph(ctx,datasets,timespan,locale){
    const config = {
        type: 'line',
        data: {
            labels: [],
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    ...timespan,
                    adapters: {
                        date:{
                            locale: locale
                        }
                    }
                },
            },
            plugins: {
                legend: {
                    display: window.innerWidth >= 600
                }
            },
            elements:{
                point:{
                    radius: 3,
                    borderWidth: 0,
                    backgroundColor: 'rgba(0,0,0,0)'
                }
            }
        }
    };
    return new Chart(ctx,config)
}