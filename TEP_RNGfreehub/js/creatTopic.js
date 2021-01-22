/**
 * Created by Think on 2018/8/8.
 */

// var ue = UE.getEditor('container');
var html;
// ue.ready(function () {
//     html = ue.getContent();
// });
axios.defaults.baseURL = 'http://127.0.0.1:8888/';

let vm = new Vue({
    el:"#content",
    data:{
        postHot:[],
        title:'',
        content:'',
        groupId:'',
        notLogin:false
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
        this.getGroupId();
        this.getGroup();
    },
    methods:{
        getGroupId(){
            this.groupId = location.href.split('=')[1];
            if(!store.state.tesssionid){
                location.href = '../../login.html';
                this.notLogin = false
            }else {
                this.notLogin = true
            }
            console.log(this.notLogin)
        },
        getGroup(){
            let that = this
            axios.get('/postList/top7',{
                }).then(function (req) {
                    console.log(req)
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

        addPost(){
            let that = this;
            that.content=editor.txt.html()
            console.log(that.content)
            var fd = new FormData()
            fd.append('title', that.title)
            fd.append('content', that.content)

            axios.post("/post",fd,{
                headers:{
                    "tsessionid":store.state.tesssionid,
                    'Content-Type': 'multipart/form-data'
                }
            }).then((res)=>{
                // console.log(res.data);
                location.href = './single-topic.html?id='+res.data.id
            }).catch((err)=>{
                console.log(err)
            })
        }
    },

});












