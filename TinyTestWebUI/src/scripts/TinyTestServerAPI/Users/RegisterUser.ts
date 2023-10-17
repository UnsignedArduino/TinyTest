import { User } from "next-auth";
import { APICallAsSystem } from "@/scripts/TinyTestServerAPI/APICall";

export default async function APIRegisterUser(userInfo: User) {
  console.log(`Registering user ${JSON.stringify(userInfo)}`);
  return await APICallAsSystem(
    "/users/register_user",
    "POST",
    JSON.stringify(userInfo),
  );
}
