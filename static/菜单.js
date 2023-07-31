// 假设获取到的数据如下
var data_list = [
    { appId: "01-0001", appName: "交叉工程类" },
    { appId: "01-0002", appName: "力学类" },
    { appId: "01-0003", appName: "机械类" },
    { appId: "01-0004", appName: "仪器类" },
    { appId: "01-0005", appName: "材料类" },
    { appId: "01-0006", appName: "能源动力类" },
    { appId: "01-0007", appName: "电气类" },
    { appId: "01-0008", appName: "电子信息类" },
    { appId: "01-0009", appName: "自动化类" },
    { appId: "01-0010", appName: "计算机类" },
    { appId: "01-0011", appName: "土木类" },
    { appId: "01-0012", appName: "水利类" },
    { appId: "01-0013", appName: "测绘类" },
    { appId: "01-0014", appName: "化工与制药类" },
    { appId: "01-0015", appName: "地质类" },
    { appId: "01-0016", appName: "矿业类" },
    { appId: "01-0017", appName: "纺织类" },
    { appId: "01-0018", appName: "轻工类" },
    { appId: "01-0019", appName: "交通运输类" },
    { appId: "01-0020", appName: "海洋工程类" },
    { appId: "01-0021", appName: "航空航天类" },
    { appId: "01-0022", appName: "兵器类" },
    { appId: "01-0023", appName: "核工程类" },
    { appId: "01-0024", appName: "农业工程类" },
    { appId: "01-0025", appName: "林业工程类" },
    { appId: "01-0026", appName: "环境科学与工程类" },
    { appId: "01-0027", appName: "生物医学工程类" },
    { appId: "01-0028", appName: "食品科学与工程类" },
    { appId: "01-0029", appName: "建筑类" },
    { appId: "01-0030", appName: "生物工程类" },
    { appId: "01-0031", appName: "公安技术类" },
    { appId: "01-0032", appName: "安全科学与工程类" },

    { appId: "02-0001", appName: "哲学类" },

    { appId: "03-0001", appName: "经济学类" },
    { appId: "03-0002", appName: "财政学类" },
    { appId: "03-0003", appName: "金融学类" },
    { appId: "03-0004", appName: "经济与贸易学类" },

    { appId: "04-0001", appName: "法学类" },
    { appId: "04-0002", appName: "政治学类" },
    { appId: "04-0003", appName: "社会学类" },
    { appId: "04-0004", appName: "民族学类" },
    { appId: "04-0005", appName: "马克思主义理论类" },
    { appId: "04-0006", appName: "公安学类" },



    { appId: "05-0001", appName: "教育学类" },
    { appId: "05-0002", appName: "体育学类" },

    { appId: "06-0001", appName: "中国语言文学类" },
    { appId: "06-0002", appName: "外国语言文学类" },
    { appId: "06-0003", appName: "新闻传播学类" },

    { appId: "07-0001", appName: "历史学类" },

    { appId: "08-0001", appName: "数学类" },
    { appId: "08-0002", appName: "物理学类" },
    { appId: "08-0003", appName: "化学类" },
    { appId: "08-0004", appName: "天文学类" },
    { appId: "08-0005", appName: "地理科学类" },
    { appId: "08-0006", appName: "大气科学类" },
    { appId: "08-0007", appName: "海洋科学类" },
    { appId: "08-0008", appName: "地球物理学类" },
    { appId: "08-0009", appName: "地质学类" },
    { appId: "08-0010", appName: "生物科学类" },
    { appId: "08-0011", appName: "心理学类" },
    { appId: "08-0012", appName: "统计学类" },

    { appId: "09-0001", appName: "植物生产类" },
    { appId: "09-0002", appName: "自然保护与环境生态类" },
    { appId: "09-0003", appName: "动物生产类" },
    { appId: "09-0004", appName: "动物医学类" },
    { appId: "09-0005", appName: "林学类" },
    { appId: "09-0006", appName: "水产类" },
    { appId: "09-0007", appName: "草学类" },

    { appId: "10-0001", appName: "基础医学类" },
    { appId: "10-0002", appName: "临床医学类类" },
    { appId: "10-0003", appName: "口腔医学类" },
    { appId: "10-0004", appName: "公共卫生与预防医学类" },
    { appId: "10-0005", appName: "中医学类" },
    { appId: "10-0006", appName: "中西医结合类" },
    { appId: "10-0007", appName: "药学类" },
    { appId: "10-0008", appName: "中药学类" },
    { appId: "10-0009", appName: "法医学类" },
    { appId: "10-0010", appName: "医学技术类" },
    { appId: "10-0011", appName: "护理学类" },

    { appId: "11-0001", appName: "管理科学与工程类" },
    { appId: "11-0002", appName: "工商管理类" },
    { appId: "11-0003", appName: "农业经济管理类" },
    { appId: "11-0004", appName: "公共管理类" },
    { appId: "11-0005", appName: "图书情报与档案管理类" },
    { appId: "11-0006", appName: "物流管理与工程类" },
    { appId: "11-0007", appName: "工业工程类" },
    { appId: "11-0008", appName: "电子商务类" },
    { appId: "11-0009", appName: "旅游管理类" },

    { appId: "12-0001", appName: "艺术学理论类" },
    { appId: "12-0002", appName: "音乐与舞蹈学类" },
    { appId: "12-0003", appName: "戏剧与影视学类" },
    { appId: "12-0004", appName: "美术学类" },
    { appId: "12-0005", appName: "设计学类" },


];
// 对数据进行分类，并设置每个类对应的文档片段
var app_list = data_list.reduce((now, v) => {
    var c = v.appId.slice(0, 2);
    if (!now.hasOwnProperty(c)) {
        now[c] = document.createDocumentFragment();
    }
    var opt = $(`<li data-value="${v.appId}"><label>${v.appName}<input type="checkbox"></label></li>`);
    // 往碎片化文档中添加的元素必须是DOM节点
    // jQuery生成的是jQuery对象，这是一个类数组对象，它的第一个元素就是对应的DOM节点
    now[c].appendChild(opt[0]);
    return now;
}, {});
// 将每个类的文档片段插入到相应的菜单中
for (var [k, v] of Object.entries(app_list)) {
    $(`.dropdown-submenu[data-index=${k}]`).find(".dropdown-menu").append(v);
}
$(".dropdown-submenu > .dropdown-menu").on('click', 'input', function (e) {
    // 当前选项的应用ID
    var nowId = $(this).parent().parent().attr("data-value");
    // 当前选项的应用名
    var nowName = $(this).parent().text();
    // 所有已选中的应用ID
    var list = !$("#checkedList").val() ? [] : $("#checkedList").val().split(" ");
    // 所有已选中的应用名
    var listName = !$("#checkedNameList").text() ? [] : $("#checkedNameList").text().split(" ");
    var index = list.indexOf(nowId);
    if ($(this).is(":checked")) {
        // 当前选项被选中，将当前选项的应用ID和应用名存入已选中的应用ID和应用名数组中
        if (index === -1) {
            list.push(nowId);
            listName.push(nowName);
        }
    } else {

        if (index !== -1) {
            list.splice(index, 1);
            listName.splice(index, 1);
        }
    }
    $("#checkedList").val(list.join(" "));
    $("#checkedNameList").text(listName.join(" "));
});
// 注意最好不要直接为label元素绑定事件，因为二级菜单的选项是动态生成的。这里没有体现出来，但实际上选项的数据是异步获取的
// 可以使用jQuery的事件代理，将事件绑定到父元素上
$(".dropdown-menu").on('click', 'label', function (e) {
    // 阻止事件冒泡到li元素，避免出现点击一个选项后列表消失的情况
    e.stopPropagation();
});
