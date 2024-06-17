<template>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <RouterLink class="navbar-brand" to="/">{{ name }}'s Book Haven</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" :to="{name: 'UserMyBooks', params: { user_id: this.user_id } }">My Books</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" :to="{name: 'UserMyRequests', params: { user_id: this.user_id } }">My Requests</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" to="/">All Books</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" :to="{name: 'UserSummary', params: { user_id: this.user_id } }">My Summary</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" v-on:click="logout" to="#">Logout</RouterLink>
                </li>
            </ul>
        </div>
    </div>
</nav>

</template>
<script>
    export default{
        name: "NavBar",
        data(){
          return{
            name:'',
            user_id: null,
          }
        },
        methods:{
            logout(){
                localStorage.clear();
                this.$router.push({name:"LogIn"});
            }
        },
        created(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
              this.name = JSON.parse(user).name,
              this.user_id = JSON.parse(user).user_id
            }
        },
    };
</script>
<style>
          .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
          }
        </style>