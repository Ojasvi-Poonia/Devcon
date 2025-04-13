import { useState,useEffect } from "react";
import { useRouter } from "next/router";
import { getMyProfile,updateProfile } from "@/utils/api";
import "@/styles/global.css"

export default function Profile() {
    const router = useRouter();
    const [user, setUser] = useState(null)
    const [form,setForm] = useState({})
    const [msg,setMsg] = useState("")
    useEffect(() => {
        const token = localStorage.getItem("token")
        if(!token){
            router.push("/auth/login")
            return
        }
        async function fetchProfile() {
            const data = await getMyProfile(token)
            if(data.email){
                setUser(data)
                setForm({
                    name: data.name || "",
                    bio: data.bio || "",
                    skills: data.skills?.join(", ")|| "",
                    college: data.college || "",
                })
            }else{
                router.push("/auth/login")
            }
        }
        fetchProfile();

    },[router])
    const handleChange = (e) => {
        setForm({...form,[e.target.name]:e.target.value})
    }
    const handleUpdate = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token")
        const updateData = {
            ...form,
            skills: form.skills.split(",").map(s => s.trim())
        }
        const res = await updateProfile(token,updateData)
        setMsg("Profile Updated")
    }
    if(!user){
        return <p>Loading Profile.....</p>
    }
    return(
        <div className="signup-wrapper">
        <form onSubmit={handleUpdate} className="signup-form">
          <h2>My Profile</h2>
          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Name"
          />
          <input
            name="college"
            value={form.college}
            onChange={handleChange}
            placeholder="College"
          />
          <input
            name="skills"
            value={form.skills}
            onChange={handleChange}
            placeholder="Skills (comma separated)"
          />
          <textarea
            name="bio"
            value={form.bio}
            onChange={handleChange}
            placeholder="Short bio"
          ></textarea>
          <button type="submit">Update Profile</button>
          {msg && <p>{msg}</p>}
        </form>
      </div>
    )
}