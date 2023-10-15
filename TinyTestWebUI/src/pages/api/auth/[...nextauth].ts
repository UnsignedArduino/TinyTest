import NextAuth, { Account, Profile, User } from "next-auth";
import { AdapterUser } from "next-auth/adapters";
import { CredentialInput } from "next-auth/providers/credentials";
import GithubProvider from "next-auth/providers/github";
import APIRegisterUser from "@/scripts/TinyTestServerAPI/Users/RegisterUser";

export const authOptions = {
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID as string,
      clientSecret: process.env.GITHUB_SECRET as string,
    }),
  ],
  pages: {
    error: "/auth/error", // Error code passed in query string as ?error=
  },
  callbacks: {
    async signIn({
      user,
    }: {
      user: User | AdapterUser;
      account: Account | null;
      profile?: Profile | undefined;
      email?: { verificationRequest?: boolean | undefined } | undefined;
      credentials?: Record<string, CredentialInput> | undefined;
    }) {
      await APIRegisterUser(user);
      return true;
    },
  },
};

export default NextAuth(authOptions);
