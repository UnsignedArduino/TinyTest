import { useSession } from "next-auth/react";
import React from "react";
import { UserAPITokenContext } from "../contexts";

export default function RequireSignedIn({
  children,
}: {
  children?: JSX.Element;
}) {
  const { status } = useSession();

  const [apiToken, setApiToken] = React.useState<string | null>(null);

  React.useEffect(() => {
    fetch("/api/auth/api-token")
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        setApiToken(json.api_token);
      });
  }, []);

  switch (status) {
    case "loading": {
      return <p>Loading...</p>;
    }
    case "unauthenticated": {
      return <p>Not signed in!</p>;
    }
    case "authenticated": {
      return (
        <UserAPITokenContext.Provider value={apiToken}>
          {children}
        </UserAPITokenContext.Provider>
      );
    }
  }
}
