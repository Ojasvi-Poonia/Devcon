import { createContext, useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import { authAPI } from "../services/api";

const AuthContext = createContext();
