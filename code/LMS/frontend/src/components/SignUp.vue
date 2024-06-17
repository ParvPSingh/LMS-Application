<template>
    <div class="error-message" v-if="error">Sorry! {{ this.error_message }}</div>
    <div>
    <div>
    <nav class="navbar bg-light">
            <div class="container-fluid center">
                <div class="row-4"></div>
                <div class="row-4">
              <span class="navbar-brand mb-0 h1"><h1>Sign Up!</h1></span>
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
                    <input class="form-control form-control-lg" type="text" name="username" placeholder="Enter Username" aria-label=".form-control-lg example" v-model="credentials.name">
                </div>
                <div class="mb-3">
                    <label for="exampleFormControlInput1" class="form-label">Email</label>
                    <input class="form-control form-control-lg" type="text" name="email" placeholder="Enter Email" aria-label=".form-control-lg example" v-model="credentials.email">
                </div>
                <div class="mb-3">
                  <label for="exampleInputPassword1" class="form-label">Password</label>
                  <input type="password" class="form-control" name="password" placeholder="Enter Password" id="exampleInputPassword1" v-model="credentials.password">
                </div>
    
                <button type="submit" class="btn btn-primary" v-on:click.prevent="signup">Sign Up</button>
              </form>
              <br>
              <h4>Already a user? <small class="text-body-secondary"><RouterLink :to="{name: 'LogIn'}">Login</RouterLink></small></h4>
        </div>
        <div class="col-4"></div>
        </div>
        </div>
        </div>
</template>
<script>
    import axios from 'axios'
    export default{
        name: 'SignUp',
        components:{
        },
        data(){
            return{
                credentials:{
                name: null,
                email: null,
                password: null,},
                error: null,
                error_message: null
            }
        },
        methods:{
            async signup(){
                try{
                let response= await axios.post("http://127.0.0.1:5000/api/user", {
                name: this.credentials.name,
                email: this.credentials.email,
                password: this.credentials.password
            });
            console.log(response);
            if(response.status==201){
                this.$router.push({name:"LogIn"});
            }else {
                    throw new Error(response.status);
                }
        } catch (error) {
                this.error = error;
                this.error_message = error.response.data.error_message
                }
            }
        },
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
