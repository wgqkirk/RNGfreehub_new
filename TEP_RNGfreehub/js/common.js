const tesssionid = this.$cookies.get("tesssionid");
let nickname = this.$cookies.get("nick_name");
let avatar = this.$cookies.get("avatar");
const userId = this.$cookies.get("user_id");
const store = new Vuex.Store({
    state:{
        tesssionid,
        nickname,
        avatar,
        notLogin:false,
        userId
    },
    mutations:{
        showname(state){
            if(!state.nickname){
                // location.href = '../../login.html';
                state.notLogin = false
            }else{
                state.notLogin = true
            }
        }

    }
})

