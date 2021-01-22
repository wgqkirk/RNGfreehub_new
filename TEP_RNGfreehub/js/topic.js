/**
 * Created by Think on 2018/8/3.
 */


axios.defaults.baseURL = 'http://127.0.0.1:8888/';

new Vue({
   el:"#content" ,
    data:{
        urlPrv:"http://127.0.0.1:8888/",
        postHot:[],
        commentList:[],
        thisPost:{},
        postDeepInfo:{},
        thiscomment:{},
        notLogin:false,
        postId:'',
        content:'',
        like:false,
        replyer:'回复',
        commentContent:'',
        showComment:'展开评论',
        showCom:false,
    },
    computed:{
        user(){
            return store.state.nickname
        },
        avatar(){
            console.log(1)
            return store.state.avatar
        }
    },
    created(){
        this.getPost();
        this.getComments();
        this.getGroup();
        this.getDeepInfo();
    },
    methods:{

        //获取这个帖子
        getPost:function(){
            let that = this;
            if(!store.state.tesssionid){
                location.href = "../templates/login.html"
            }
            that.postId = location.href.split('=')[1];
            axios.get("/post/"+that.postId+"/",{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then((req)=>{
                that.thisPost = req.data;
                that.notLogin = true
            }).catch((err)=>{
                console.log(err);
                that.notLogin = false
            })
        },
        getGroup(){
            let that = this
            axios.get('/postList/top7',{
                }).then(function (req) {
                that.postHot = req.data.street_list.data.list;
                if(store.state.tesssionid){
                    that.notLogin = true
                }else {
                    that.notLogin = false
                }
                }).catch(function (err) {
                    console.log(err)
                });
        },
        //获取评论
        getComments:function () {
            let that = this;
            axios.get("post/"+that.postId+"/comment/",{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then((req)=>{
                that.thiscomment = req.data;
                that.commentList = req.data.commentList

            }).catch((err)=>{
                console.log(err)
            })
        },
        getDeepInfo:function(){
            let that = this;
            that.postId = location.href.split('=')[1];
            axios.get("/postDeepInfo/"+that.postId+"/",{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then((req)=>{
                that.postDeepInfo = req.data;
                that.notLogin = true
            }).catch((err)=>{
                console.log(err);
                that.notLogin = false
            })
        },
        //点击回复
        replyaa:function(id,name){
              this.replyer = `回复${name}`;
              this.thisPost.user.id = id;
        },
        //回复请求
        addReplys:function (index,commId) {
            let that = this;
            axios.post('/comments/'+commId+'/replys/',{
                "content":that.content,
                "replyed_user":that.thisPost.user.id
            },{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then((req)=>{
                that.content = '';
                that.getCommToComm(index,commId)
            })
        },
        //点赞
        addLike:function (id,index) {
            let that = this;
            axios.post('/comments/'+id+'/likes/',{},{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then((req)=>{
                that.like = true;
               Vue.set(that.thiscomment[index],'like_nums', 1 + that.thiscomment[index].like_nums);
            }).catch((err)=>{

            })
        },
        addComment:function () {
            let that = this;
            axios.post("/post/"+that.postId+"/comment/",{
                "content":that.commentContent
            },{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then((req)=>{
                that.getComments();
                that.getDeepInfo();
                console.log(222)
                that.commentContent ='';
                that.postDeepInfo='';

            }).catch((err)=>{
                console.log(err)
            })
        },
        getCommToComm:function (index,id) {
            let that = this;
            axios.get('/comments/'+id+'/replys/',{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then((req)=>{
                Vue.set(that.thiscomment[index],"commToComm",req.data);
            }).catch((err)=>{
                console.log(err)
            })
        },
        showedComment:function (index,commentId) {
            let that = this;
            if(that.thiscomment[index]['showCom'] === true){
                that.thiscomment[index]['showComment'] = '展开评论';
                Vue.set(that.thiscomment[index],"showCom",false);
            }else {
                that.thiscomment[index]['showComment'] = '收起评论';
                for(let i = 0; i<that.thiscomment.length; i++){
                    Vue.set(that.thiscomment[i],['showCom'] , false)
                }
                Vue.set(that.thiscomment[index],"showCom",true);
                that.getCommToComm(index,commentId);
            }
        },
        showReply:function () {
            console.log(11)
          $('#reply_box').removeAttr("style");
        }
    },

});

