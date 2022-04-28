//auto.js 自动重启
let process = require('child_process');
let fs = require('fs-extra');
let ChildProcess  = process.fork('./app.js');

ChildProcess.on('exit',function (code) {
    console.log('process exits + '+code);
    fs.appendFileSync('./log.txt','线程退出');
    if(code !== 0){
        process.fork('./auto.js');
    }
});