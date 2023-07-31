$(".dropdown-menu").on('click', 'label', function (e) {
    // 阻止事件冒泡到li元素，避免出现点击一个选项后列表消失的情况
    e.stopPropagation();
});