var baseUrl = '';

var code_add = function() {

    $("#register_form").validate({
        submitHandler: function(form) {

            var f = confirm("자산 정보를 등록하시겠습니까?");
            if(f){
                form.submit();
            } else {
                return false;
            }
        },
        rules: {
            code_category_id: {
                required: true
            },
            code_name: {
                required: true,
                minlength: 1
            },
        },
        //규칙체크 실패시 출력될 메시지
        messages : {
        }
    });
}

var code_updform = function () {

    var code_id = $(this).attr('value');
    $.ajax({
        type: 'get',
        url: baseUrl + '/e/code/updform/' + code_id,
        success: function (data) {
            $("#myModalLabel").html('코드 정보 : ' + data.code.category_name + ' > ' + data.code.code_name);
            $("#modal_code_id").val(data.code.id);
            $("#modal_code_name").val(data.code.code_name);

            var str_code_category_list;
            if (data.code_category_list.length > 0) {
                str_code_category_list = '<select name="modal_code_category_id" id="modal_code_category_id" class="selectpicker show-tick form-control" data-live-search="true" title="Choose one of the following..." data-live-search-placeholder="Search...">';
                $.each(data.code_category_list, function () {
                    str_code_category_list += '<option value="' + this.id + '">' + this.category_name + '</option>';

                });
                str_code_category_list += '</select>';
            } else {
                str_code_category_list = '등록된 코드 분류가 없습니다.';
            }

            $("#code_category_list").html(str_code_category_list);

            $('#modal_code_category_id').selectpicker();
            $('#modal_code_category_id').selectpicker('val', data.code.category_id);

            $("#myModal").modal("show");
        },
        error: function (xhr, status, error) {
            alert("code:" + xhr.status);
            alert(status);
            alert(error);
        },
    });
}

var code_upd = function() {

    $("#register_form").validate({
        submitHandler: function(form) {
            $.ajax({
                type : 'post',
                url : baseUrl + '/e/code/upd/',
                data : {
                    modal_code_category_id: $("#modal_code_category_id").val(),
                    modal_code_id: $("#modal_code_id").val(),
                    modal_code_name: $("#modal_code_name").val(),
                },
                success : function() {
                    alert("코드 정보가 수정되었습니다.");
                    location.reload();
                },
                error: function (xhr, status, error) {
                    alert("code:" + xhr.status);
                    alert(status);
                    alert(error);
                },
            });
        },
        rules: {
            modal_category_code_id: {
                required: true,
                minlength: 1
            },
            modal_code_id: {
                required: true
            },
            modal_code_name: {
                required: true,
                minlength: 1
            }
        },
        //규칙체크 실패시 출력될 메시지
        messages : {
        },
    });
}

var equip_history_updform = function () {

    var history_id = $(this).attr('value');

    $.ajax({
        type: 'get',
        url: baseUrl + '/e/equip/history/view/' + history_id + '/',
        success: function (data) {
            $("#myModalLabel").html('장비 사용이력 : ' + data.history.equipment_name);
            $("#history_id").val(data.history.id);
            $("#user_name").val(data.history.user_name);
            var str_start_ymd = data.history.start_ymd.slice(0,4) + '-' + data.history.start_ymd.slice(4,6) + '-' + data.history.start_ymd.slice(6,8);
            $("#start_ymd").val(str_start_ymd);
            var str_end_ymd = data.history.end_ymd.slice(0,4) + '-' + data.history.end_ymd.slice(4,6) + '-' + data.history.end_ymd.slice(6,8);
            $("#end_ymd").val(str_end_ymd);

            var str_project_list;
            if (data.project_list.length > 0) {
                // str_project_list = '<select name="project_id" data-live-search="true">';
                str_project_list = '<select name="project_id" id="project_id" class="selectpicker show-tick form-control" data-live-search="true" title="Choose one of the following..." data-live-search-placeholder="Search...">';
                $.each(data.project_list, function () {

                    str_project_list += '<option value="' + this.id + '">' + this.project_name + '</option>';
                });
                str_project_list += '</select>';
            } else {
                str_project_list = '등록된 프로젝트가 없습니다.';
            }

            $("#project_list").html(str_project_list);

            $('.selectpicker').selectpicker();
            $('.selectpicker').selectpicker('val', data.history.project_id);

            $("#myModal").modal("show");
        },
        error: function (xhr, status, error) {
            alert("code:" + xhr.status);
            alert(status);
            alert(error);
        },
    });
}

var equip_history_addform = function () {

    var history_id = 0;
    var equipment_name = $(this).attr('value');

    $.ajax({
        type: 'get',
        url: baseUrl + '/e/equip/history/view/' + history_id + '/',
        success: function (data) {
            $("#myModalLabel").html('자산 사용이력 : ' + equipment_name);
            $("#user_name").val(data.history.user_name);
            $("#start_ymd").val(data.history.start_ymd);
            $("#end_ymd").val(data.history.end_ymd);

            var str_project_list;
            if (data.project_list.length > 0) {
                str_project_list = '<select name="project_id" id="project_id" class="selectpicker show-tick form-control" data-live-search="true" title="Choose one of the following..." data-live-search-placeholder="Search...">';
                $.each(data.project_list, function () {
                    str_project_list += '<option value="' + this.id + '">' + this.project_name + '</option>';
                });
                str_project_list += '</select>';
            } else {
                str_project_list = '등록된 프로젝트가 없습니다.';
            }

            $("#project_list").html(str_project_list);

            $('.selectpicker').selectpicker();
            $('.selectpicker').selectpicker('val', data.history.project_id);

            $("#myModal").modal("show");
        },
        error: function (xhr, status, error) {
            alert("code:" + xhr.status);
            alert(status);
            alert(error);
        },
    });
}

var equip_history_upd = function() {

    var history_id = $("#history_id").val();
    var equipment_id = $("#equipment_id").val();
    if (history_id.length < 1) history_id = '0';

    $("#register_form").validate({
        rules: {
            project_id: {
                required: true
            },
            user_name: {
                required: true
            },
            start_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            },
            end_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            }
        },
        //규칙체크 실패시 출력될 메시지
        messages : {
            start_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            },
            end_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            }
        },
        submitHandler: function(form) {
            $.ajax({
                type : 'post',
                url : baseUrl + '/e/equip/history/upd/' + history_id + '/',
                data : {
                    equipment_id: equipment_id,
                    history_id: history_id,
                    project_id: $("#project_id").val(),
                    user_name: $("#user_name").val(),
                    start_ymd: $("#start_ymd").val(),
                    end_ymd: $("#end_ymd").val(),
                },
                success : function() {
                    alert("사용이력이 등록(수정)되었습니다.");
                    location.reload();
                },
                error: function (xhr, status, error) {
                    alert("code:" + xhr.status);
                    alert(status);
                    alert(error);
                },
            });
        }
    });
}

var doGoBack = function() {

    history.back();
}

var equip_add = function() {

    $("#register_form").validate({
        submitHandler: function(form) {

            var f = confirm("자산 정보를 등록하시겠습니까?");
            if(f){
                form.submit();
            } else {
                return false;
            }
        },
        rules: {
            equipment_code: {
                required: true
            },
            manufacturer_code: {
                required: true
            },
            state_code: {
                required: true
            },
            model_no: {
                required: true,
                minlength: 1
            },
            serial_no: {
                required: true,
                minlength: 1
            },
            purchase_price: {
                required: true,
                digits: true,
                minlength: 1
            },
            purchase_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            },
            discard_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            }
        },
        //규칙체크 실패시 출력될 메시지
        messages : {
            purchase_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            },
            discard_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            }
        }
    });
}

var equip_upd = function() {

    $("#register_form").validate({
        submitHandler: function(form) {

            var f = confirm("자산 정보를 수정하시겠습니까?");
            if(f){
                form.submit();
            } else {
                return false;
            }
        },
        rules: {
            equipment_code: {
                required: true
            },
            manufacturer_code: {
                required: true
            },
            state_code: {
                required: true
            },
            model_no: {
                required: true,
                minlength: 1
            },
            serial_no: {
                required: true,
                minlength: 1
            },
            purchase_price: {
                required: true,
                digits: true,
                minlength: 1
            },
            purchase_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            },
            discard_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            }
        },
        //규칙체크 실패시 출력될 메시지
        messages : {
            purchase_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            },
            discard_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            }
        }
    });
}

var project_add = function() {

    $("#register_form").validate({
        submitHandler: function(form) {

            var f = confirm("프로젝트 정보를 등록하시겠습니까?");
            if(f){
                form.submit();
            } else {
                return false;
            }
        },
        rules: {
            project_name: {
                required: true,
                minlength: 1
            },
            start_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            },
            end_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            },
        },
        //규칙체크 실패시 출력될 메시지
        messages : {
            start_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            },
            end_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            }
        }
    });
}

var project_updform = function () {

    var project_id = $(this).attr('value');
    $.ajax({
        type: 'get',
        url: baseUrl + '/e/pjt/updform/' + project_id + '/',
        success: function (data) {
            $("#myModalLabel").html('프로젝트 정보 : ' + data.project.project_name);
            $("#modal_project_id").val(data.project.id);
            $("#modal_project_name").val(data.project.project_name);

            var str_start_ymd = data.project.start_ymd.slice(0,4) + '-' + data.project.start_ymd.slice(4,6) + '-' + data.project.start_ymd.slice(6,8);
            $("#modal_start_ymd").val(str_start_ymd);

            var str_end_ymd = data.project.end_ymd.slice(0,4) + '-' + data.project.end_ymd.slice(4,6) + '-' + data.project.end_ymd.slice(6,8);
            $("#modal_end_ymd").val(str_end_ymd);

            $("#myModal").modal("show");
        },
        error: function (xhr, status, error) {
            alert("code:" + xhr.status);
            alert(status);
            alert(error);
        },
    });
}

var project_upd = function() {

    $("#register_form").validate({
        rules: {
            modal_project_name: {
                required: true,
                minlength: 1
            },
            modal_start_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            },
            modal_end_ymd: {
                required: true,
                dateISO: true,
                minlength: 10
            },
        },
        //규칙체크 실패시 출력될 메시지
        messages : {
            modal_start_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            },
            modal_end_ymd: {
                required: "필수 항목입니다.",
                dateISO: "yyyy-MM-dd 형식이어야 합니다."
            }
        },
        submitHandler: function(form) {
            $.ajax({
                type : 'post',
                url : baseUrl + '/e/pjt/upd/',
                data : {
                    modal_project_id: $("#modal_project_id").val(),
                    modal_project_name: $("#modal_project_name").val(),
                    modal_start_ymd: $("#modal_start_ymd").val(),
                    modal_end_ymd: $("#modal_end_ymd").val(),
                },
                success : function() {
                    alert("프로젝트 정보가 수정되었습니다.");
                    location.reload();
                },
                error: function (xhr, status, error) {
                    alert("code:" + xhr.status);
                    alert(status);
                    alert(error);
                },
            });
        }
    });
}
