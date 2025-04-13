import { useState,useEffect } from "react";
import { useRouter } from "next/router";
import { getMyProfile,updateProfile } from "@/app/utils/api";
import "@/app/styles/global.css"

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
}