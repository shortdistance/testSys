from flask import render_template, jsonify
from scripts.services import monitor
from . import bp_main as main


@main.route('/Monitor', methods=['GET'])
def mon_list():
    return render_template('Mon/List.html')


@main.route('/Monitor/GetData', methods=['GET'])
def getCpuData():
    cpuInfo = []
    memInfo = []

    cpuInfo, memInfo = monitor.getDataAll()
    return jsonify(cpuInfo=cpuInfo, memInfo=memInfo)
