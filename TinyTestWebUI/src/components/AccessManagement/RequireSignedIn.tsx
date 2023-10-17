import { useSession } from "next-auth/react";
import React from "react";

export default function RequireSignedIn({
  children,
}: {
  children?: JSX.Element;
}) {
  const { status } = useSession();

  switch (status) {
    case "loading": {
      return <p>Loading...</p>;
    }
    case "unauthenticated": {
      return <p>Not signed in!</p>;
    }
    case "authenticated": {
      return children;
    }
  }
}
