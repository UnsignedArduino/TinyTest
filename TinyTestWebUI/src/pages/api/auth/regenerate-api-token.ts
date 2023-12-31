import type { NextApiRequest, NextApiResponse } from "next";
import { getServerSession } from "next-auth/next";
import { authOptions } from "./[...nextauth]";
import { APICallAsSystem } from "@/scripts/TinyTestServerAPI/APICall";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const session = await getServerSession(req, res, authOptions);
  // @ts-ignore
  const id = session.user.id;

  if (session) {
    res
      .status(200)
      .json(
        await (
          await APICallAsSystem("/users/id_regenerate_api_token", "POST", id)
        ).json(),
      );
  } else {
    res.status(401).json({ message: "Not signed in!" });
  }
}
