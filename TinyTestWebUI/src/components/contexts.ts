import React from "react";

export interface UserInterface {
  apiToken: string;
  verified: boolean;
  admin: boolean;
}

export const UserContext = React.createContext<UserInterface | null>(null);
