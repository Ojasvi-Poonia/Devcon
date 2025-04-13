import { useState } from "react";
import { useRouter } from "next/router";
import { signup } from "../../utils/api";
import "@/app/styles/signup.css"

export default function Signup() { // component signup
    const router = useRouter();
    const [form,setForm] = useState({name: "" , email: "", password: ""});
    const [error,setError] = useState("");
    const handleChange = (e) => {
        setForm({...form,[e.target.name]: e.target.value});     //we use ...name bcz we can directly update a particular thing wihout messing up the others
    };
    const handleSubmit = async (e) => {
        e.preventDefault(); //Normally when we reload we loose every piece of data so it keeps data with itself
        const res = await signup(form)
        if(res.message == "User registered"){
            router.push("/auth/login")
        }else{
            setError(res.detail || "Signup Failed")
        }
    };
    return(
        <div className="signup-wrapper">
            <form onSubmit={handleSubmit} className="signup-form">
                <h2>SignUp</h2>
                <input name="name" placeholder="Name" onChange={handleChange} required/>
                <input name="email" type="email" placeholder="Email" onChange={handleChange} required/>
                <input name="password" type="password" placeholder="Password" onChange={handleChange} required/>
                <button type="submit">Register</button>
                {error && <p className="error">{error}</p>}
            </form>
        </div>
    )
}