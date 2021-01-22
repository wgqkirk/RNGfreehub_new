axios.defaults.baseURL = 'http://127.0.0.1:8888/';
var vm = new Vue({
    el:'#content',
    data:{
        credential:'',
        password:'',
        account:false,
        datapsw:'',
        datamobile:''
    },
    methods:{
        login: function() {
            this.getcookie();
            let that = this;
            let reg = /^[1][3,4,5,7,8][0-9]{9}$/;
			console.log(that.credential)
			console.log(this.password.length)
			console.log(this.password.length)
            if(!reg.test(that.credential) || this.password.length < 6 || this.password.length>20){
                alert('请填写正确的信息！')
            }else{
                axios.post('/login/',{
                    'credential':that.credential,
                    'password':that.password
                }).then((res)=>{
                    console.log(res.data);
                    this.$cookies.set('tesssionid',res.data.token);
                    this.$cookies.set('nick_name',res.data.nick_name);
                    this.$cookies.set('avatar',res.data.avatar);
                    this.$cookies.set('user_id',res.data.id);
                    location.href = '../templates/index.html'

                }).catch(function (err) {
                    console.log(err);
                    if(err.response.status === 400){
                        if(err.response.data.non_fields){
                            that.datapsw = err.response.data.non_fields;
                            that.datamobile = ''
                        }else if(err.response.data.credential){
                            that.datapsw = '';
                            that.datamobile = err.response.data.credential
                        }
                    }
                })
            }
        },
        changeMobile:function(){
            let that = this;
            let reg = /^[1][3,4,5,7,8][0-9]{9}$/;
            if(!reg.test(that.credential)){
                this.account = '请输入正确的手机号!';

            }else{
                that.account = '';

            }
        },
        setCookie:function (userId) {
            let str = 'token = '+userId;
            document.cookie = str;
        },
        getcookie:function () {
            let cookies = document.cookie;
            let cookiesArr = cookies.split(';');
            cookiesArr.forEach(function (value, index, array) {
                var a = 'userId';
               if(value.indexOf(a)){
                   console.log(value);
                    return
               }
            });
        }
    }
});

