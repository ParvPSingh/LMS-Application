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
                    <RouterLink class="nav-link" aria-current="page" to="/librarian_request_page">Request Page</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" to="/librarian_feedback_page">Feedback Page</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" to="/librarian_userinfo">User Info</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" to="/librarian_summary">Highlights</RouterLink>
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
    name: "LibrarianNavbar",
    data(){
          return{
            name:''
          }
        },
    methods:{
        logout(){
            localStorage.clear();
            this.$router.push({name:"LogIn"});
        }
    },
    mounted(){
            let user= localStorage.getItem('userInfo');
            if(user!=null){
              this.name = JSON.parse(user).name
            }
        }
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