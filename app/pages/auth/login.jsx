import { use, useState } from "react";
import { useRouter } from "next/router";
import { login } from "../../utils/api";
import "@/app/styles/signup.css"

export default function Login(){
    const router = useRouter()
    const [form, setForm] = useState({email: "",password: ""})
    const [error,setError] = useState("")
    const handleChange = (e) => {
        setForm({...form,[e.target.name]:[e.target.value]})
    }
    const handleSubmit = async (e) => {
        e.preventDefault()
        const res = await login(form)
        if(res.access_token){
            localStorage.setItem("token",res.access_token)
            router.push("/profile")

        }else{
            setError(res.detail || "Login Failed")
        }
    }
    return(
        <div className="signup-wrapper">
        <form onSubmit={handleSubmit} className="signup-form">
          <h2>Login</h2>
          <input
            name="email"
            type="email"
            placeholder="Email"
            onChange={handleChange}
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            onChange={handleChange}
            required
          />
          <button type="submit">Login</button>
          {error && <p className="error">{error}</p>}
        </form>
      </div>
    )
}
