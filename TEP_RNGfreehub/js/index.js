/**
 * Created by Think on 2018/7/14.
 */
axios.defaults.baseURL = 'http://127.0.0.1:8888/';

let vm = new Vue({
    el:"#content",
    data:{
        postlist:[],
        noticelist:[],
        notice_count:'',
        token:'',
    },
    computed:{
        user(){
            return store.state.nickname
        },
        notLogin(){
            return store.state.notLogin
        },
        avatar(){
            console.log(1)
            return store.state.avatar
        }
    },
    created(){
        this.showname();
        this.posts();
        this.notice();
    },
    methods:{
        showname(){
            return store.commit('showname')
        },
        posts(){
            let that = this;
            axios.get('/postList',{
            }).then(function (req) {
                that.postlist = req.data.street_list.data.list;
                // console.log(that.postlist)
            }).catch(function (err) {
                console.log(err)
            })
        },
        notice(){
            let that = this;
            axios.get('/post/notice/',{
                headers:{
                    tsessionid: store.state.tesssionid
                }
            }).then(function (req) {
                console.log(req)
                that.noticelist = req.data.data;
                that.notice_count=req.data.total;
                // console.log(that.postlist)
            }).catch(function (err) {
                console.log(err)
            })
        }
    }
});

