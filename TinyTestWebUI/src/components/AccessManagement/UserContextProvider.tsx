import { useSession } from "next-auth/react";
import React from "react";
import { UserContext, UserInterface } from "../contexts";
import { APICallDirectAsUser } from "@/scripts/TinyTestServerAPI/APICall";

export default function UserContextProvider({
  children,
}: {
  children?: JSX.Element;
}) {
  const { data: session } = useSession();

  const [userContext, setUserContext] = React.useState<UserInterface | null>(
    null,
  );

  React.useEffect(() => {
    setUserContext(null);
    if (!session) {
      return;
    }
    let apiToken: string = "";
    fetch("/api/auth/api-token")
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        apiToken = json.api_token;
      })
      .then(() => {
        return APICallDirectAsUser(
          // @ts-ignore
          `/users/roles?user_id=${session.user.id}`,
          "GET",
          undefined,
        );
      })
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        setUserContext({
          apiToken: apiToken,
          verified: json.verified,
          admin: json.admin,
        });
      });
  }, [session]);

  return (
    <UserContext.Provider value={userContext}>{children}</UserContext.Provider>
  );
}
