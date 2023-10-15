import { User } from "next-auth";
import APICall from "@/scripts/TinyTestServerAPI/APICall";

export default async function APIRegisterUser(userInfo: User) {
  console.log(`Registering user ${JSON.stringify(userInfo)}`);
  return await APICall(
    "/users/register_user",
    "POST",
    JSON.stringify(userInfo),
  );
}
