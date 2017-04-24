<!DOCTYPE html>
<html lang="zh-CN">
    <head>
          <meta charset="UTF-8">
          <!-- 获取显示器的物理行高，进行适配 -->
          <meta name="viewport" content="width=device-width, initial-scale=1">         
           <!-- 新 Bootstrap 核心 CSS 文件 -->
            <link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css"> 
          <!-- 可选的Bootstrap主题文件(一般不用引入) -->
            <link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
          <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
           <script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
          <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
           <script src="//cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
          
           <link rel="stylesheet" type="text/css" href="../static/css/sty1.css" />
    </head>
    <body>
        <nav class="navbar navbar-inverse navbar-fixed-top">
            <div class="container-fluid">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="#">运维管理平台</a>
                    <a class="navbar-brand btn zhuce" data-toggle="modal" data-target="#exampleModal" data-whatever="@mdo" id="btn-update">账号注册</a>
            
                </div>
                <div id="navbar" class="navbar-collapse collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="#">当前登陆!</a></li>
                        {% for user in name.items() %}
                        <li><a href="#">{{user[1]}}</a></li>
                        {% endfor %}
                        <li><a href="/Exit/">登出!</a></li>
                    </ul>
       
                </div>
                </div>
        </nav>

        <div class="container-fluid">
          <div class="row">
          <!-- zuoce.css-->
            <div class="col-sm-3 col-md-2 sidebar zuoce">
                <ul class="nav nav-sidebar">
                    <li class="active"><a href="#">服务器资产 <span class="sr-only">(current)</span></a></li>
                    <li><a href="#">IDC</a></li>
                    <li><a href="#">机柜</a></li>
                    <li><a href="#">监控</a></li>
                </ul>
                    <ul class="nav nav-sidebar">
                        <li><a href="">日志分析</a></li>
                        <li><a href="">Nav item again</a></li>
                        <li><a href="">One more nav</a></li>
                        <li><a href="">Another nav item</a></li>
                        <li><a href="">More navigation</a></li>
                </ul>
                    <ul class="nav nav-sidebar">
                        <li><a href="">Nav item again</a></li>
                        <li><a href="">One more nav</a></li>
                        <li><a href="">Another nav item</a></li>
                    </ul>
            </div>
             <!-- youce-->
             <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main youce">
                <h1 class="page-header">Dashboard</h1>

                 <div class="row placeholders">
                    <div class="col-xs-6 col-sm-3 placeholder">
                    <!-- <span class="text-muted">Something else</span> -->
                    <form class="add" action="/increase/" method="post">
                        <span><input type="submit" class="text-muted btn btn-success" value="增加" /><span>
                    </form>

                </div>
                    <div class="col-xs-6 col-sm-3 placeholder">
                    <form class="delete" action="/delete/" method="post">
                        <span><input type="submit" class="text-muted btn btn-danger" value="删除" /></span>
                    </form>

                </div>
                    <div class="col-xs-6 col-sm-3 placeholder">
                    <form class="update" action="/update/" method="post">
                        <span><input type="submit" class="text-muted btn btn-warning" value="修改" /></span>
                    </form>
                                                                                                                                                                                                                         </div>
                    <div class="col-xs-6 col-sm-3 placeholder">
                    <form class="selete" action="/select/" method="post">
                        <span><input type="submit" class="text-muted btn btn-info" value="查询" /></span>
                     </form>

                    </div> 
             </div>

                     <div class="table-responsive">
                     <table class="table table-striped"> 
                 <thead>
                     <tr>
                       <th>id编号</th>
                       <th>用户名</th>
                       <th>密码</th>
                       <th>年龄</th>
                       <th>Email</th>
                       <th>手机</th>
                       <th>操作</th>
                     </tr>
                 </thead>
                 <tbody> 
                          {% for user in pages %}
                       <tr>
                             <td>{{user[0]}}</td>
                             <td>{{user[1]}}</td>
                             <td>{{user[2]}}</td>
                             <td>{{user[3]}}</td>
                             <td>{{user[4]}}</td>
                             <td>{{user[5]}}</td>
                             <td>

<!-- <button type="button" class="btn btn-link btn-warning" data-toggle="modal" data-target="#updateDialog" data-id="{{user[0]}}"data-username="{{user[1]}}" data-password="{{user[2]}}" data-age="{{user[3]}}" data-email="{{user[4]}}" data-IPhone="{{user[5]}}" >修改
</button> -->
<!-- 测试 点击修改位置-->
<a class="btn btn-warning" data-toggle="modal"  data-target="#exampleModal"  data-id="{{user[0]}}" data-username="{{user[1]}}" data-password="{{user[2]}}" data-age="{{user[3]}}" data-email="{{user[4]}}" data-IPhone="{{user[5]}}" id="btn-xiugai">修改</a>
<a class="btn btn-danger" href="/deleteUser/?id={{user[0]}}">删除</a>
        </div>
</td> 
                           {% endfor %}
                       </tr>
         <!-- 分页 start-->
<!--            <nav>
                <ul class="pagination">
                    <li>
                      <a href="#" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                      </a>
                    </li>
                       <li><a href="#">1</a></li>
                       <li><a href="#">2</a></li>
                       <li><a href="#">3</a></li>
                       <li><a href="#">4</a></li>
                       <li><a href="#">5</a></li>
                    <li>
                       <a href="#" aria-label="Next">
                           <span aria-hidden="true">&raquo;</span>
                       </a>
                    </li>
                  </ul>
           </nav>   -->

         <!-- 分页 end -->
         <!-- 账号注册部分 -->
         <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                        <h4 class="modal-title" id="exampleModalLabel">添加用户</h4>
                    </div> 

                    <div class="modal-body">
                        <form>
                        <div class="form-group">
                            <label for="username" class="control-label">用户</label>
                            
                                <input type="text" class="form-control" id="username" name='username'>
                            </div>
         

                        <div class="form-group">
                            <label for="password" class="control-label">密码</label>
                            
                                <input type="text" class="form-control" id="password" name='password'>
                            </div>
                        

                      <div class="form-group">
                          <label for="age" class="control-label">年龄</label>
                          
                              <input type="text" class="form-control" id="age" name='age'>
                          </div>
                      

                      <div class="form-group">
                          <label for="email" class="control-label">邮箱</label>
                         
                              <input type="text" class="form-control" id="email" name='email'>
                          </div>
                      

                      <div class="form-group">
                          <label for="IPhone" class="col-sm-2 control-label">手机</label>
                          
                              <input type="text" class="form-control" id="IPhone" name='IPhone'>
                          </div>
                     

                    </form>
                 </div>
                 <div class="modal-footer">
                     <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
                     <button type="button" class="btn btn-primary" id="btn-add">添加</button>
                     <!-- 测试部分    点击弹出窗口点击修改-->
                     <button type="button" class="btn btn-warning" id="btn-xiugai1">修改</button>
                 </div>
               </div>
             </div>
           </div>
           <!-- 账号注册部分 end -->
           <!--  注册账号Ajax -->
           <script type="text/javascript">
           jQuery(document).ready(function(){
               jQuery('#btn-update').on('show.bs.modal', function (event) {
                    var button = jQuery(event.relatedTarget)
                    var recipient = button.data('whatever')
                    var modal = jQuery(this)
                    modal.find('modal-title').text('New username to ' + recipient)
                    modal.find('modal-body input').val(recipient)
                    });
                    jQuery('#btn-add').on('click', function() {
                        var username = jQuery('#username').val(),
                            password = jQuery('#password').val(),
                            age = jQuery('#age').val(),
                            email = jQuery('#email').val(),
                            IPhone = jQuery('#IPhone').val()
                            jQuery.post('/adduser/', {
                                'username' : username,
                                'password' : password,
                                'age' : age,
                                'email' : email,
                                'IPhone' : IPhone
                            }, function(data) {
                                console.log(data);
                                if(data['ok']) {
                                    jQuery('#btn-update').modal('hide');
                                    window.location.reload();
                                } else {
                                    jQuery('#error').text(data['result']);
                                    jQuery('#error').show();
                                }
                            }, 'json');
               
               
               /* <!-- 点击修改模态框测试 修改 --> */
               jQuery('#btn-xiugai').on('show.bs.modal', function (event) {
                    var button = jQuery(event.relatedTarget)
                    var recipient = button.data('whatwver')
                    var modal = jQuery(this)
                    
                    modal.find('modal-title').text('修改用户' + recipient)
                    modal.find('modal-body input').val(recipient)
                    });
                    modal.find('#username').val(button.data('username'));
                    modal.find('#password').val(button.data('password'));
                    modal.find('#age').val(button.data('age'));
                    modal.find('#email').val(button.data('email'));
                    modal.find('#IPhone').val(button.data('IPhone'));
                    });
                    jQuery('#btn-xiugai1').on('click', function() {
                    var  username = jQuery('#username').val(),
                            password = jQuery('#password').val(),
                            age = jQuery('#age').val(),
                            email = jQuery('#email').val(),
                            IPhone = jQuery('#IPhone').val()
                            jQuery.post('/updateone/', {
                                'username' : username,
                                'password' : password,
                                'age' : age,
                                'emial' : email,
                                'IPhone' : IPhone
                            }, function(data) {
                                console.log(data);
                                if(data['ok']) {
                                    jQuery('#btn-xiugai').modal('hide');
                                    window.location.reload();
                                  
                                } else {
                                    jQuery('#error').text(data['result']);
                                    jQuery('#error').show();
                                }
                            }, json);
                      });
 
                    });
                });
           </script>
       </body>
</html>
