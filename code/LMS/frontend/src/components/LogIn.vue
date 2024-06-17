<template>
    <div>
        <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
        <nav class="navbar bg-light">
            <div class="container-fluid center">
                <div class="row-4"></div>
                <div class="row-4">
              <span class="navbar-brand mb-0 h1"><h1>Login</h1></span>
              </div>
              <div class="row-4"></div>
            </div>
        </nav>
        <div class="row">
            <div class="col-4"></div>
        <div class="col-4">
            <form>
                <div class="mb-3">
                    <label for="exampleFormControlInput1" class="form-label">Username</label>
                    <input class="form-control form-control-lg" type="text" name="username" placeholder="Enter Username" v-model="credentials.name" aria-label=".form-control-lg example">
                </div>
                <div class="mb-3">
                    <label for="exampleFormControlInput1" class="form-label">E-mail</label>
                    <input class="form-control form-control-lg" type="text" name="email" placeholder="Enter E-mail" v-model="credentials.email" aria-label=".form-control-lg example">
                </div>
                <div class="mb-3">
                    <label for="exampleInputPassword1" class="form-label">Password</label>
                    <input type="password" class="form-control" name="password" placeholder="Enter Password" v-model="credentials.password" id="exampleInputPassword1">
                </div>

                <button type="submit" v-on:click.prevent="login" class="btn btn-primary">Submit</button>
            </form>
            <br>
              <h4>Not a user? <small class="text-body-secondary"><RouterLink :to="{name: 'SignUp'}">Signup</RouterLink></small></h4>
        </div>
        <div class="col-4"></div>
            </div>
    </div>
</template>
<script>
import axios from 'axios'
    export default{
        name: 'LogIn',
        components:{
        },
        data(){
            return{
                credentials:{
                name: null,
                email: null,
                password: null,},
                user_role : null,
                error : null,
                error_message: null,
            }
        },
        methods:{
            async login(){
                try{
                let response = await axios.post("http://127.0.0.1:5000/login_user", {
                name: this.credentials.name,
                email: this.credentials.email,
                password: this.credentials.password
            });
            console.warn(response);
            if(response.status==200){
                console.log(response)
                this.user_role = response.data.role
                let token = JSON.stringify(response.data.token)
                if(token){
                    localStorage.setItem("userInfo", JSON.stringify(response.data));
                }
                let user= localStorage.getItem('userInfo');
                if (user) {
                    let role = JSON.parse(user).role
                    if (role == "user") {
                        this.$router.push({ name: 'HomePage' })
                    }
                    if (role == "librarian") {
                        this.$router.push({ name: 'LibrarianDashboard' })
                    }
                }
                
            }
        }
        catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                this.$router.push({ name: 'LogIn' })
                }
        }
        },
        mounted(){
            let user= localStorage.getItem('userInfo');
            if (user) {
                let role = JSON.parse(user).role
                console.log(role)
                if (role == "user") {
                    this.$router.push({ name: 'HomePage' })
                }
                if (role == "librarian") {
                    this.$router.push({ name: 'LibrarianDashboard' })
                }
            }
        }
    }
</script>
<style>
.error-message {
    background-color: #f44330;
    color: #fff;
    padding: 10px;
    margin: 0 auto;
    width: 50%;
    text-align: center;
    border-radius: 5px; 
    opacity: 0; 
    animation: fadeIn 0.5s ease forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
          .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
          }
        </style>
