import NextAuth, { Account, Profile, Session, User } from "next-auth";
import { AdapterUser } from "next-auth/adapters";
import { CredentialInput } from "next-auth/providers/credentials";
import GithubProvider from "next-auth/providers/github";
import APIRegisterUser from "@/scripts/TinyTestServerAPI/Users/RegisterUser";
import { JWT } from "next-auth/jwt";

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
    async jwt({
      token,
      profile,
    }: {
      token: JWT;
      user: User | AdapterUser;
      account: Account | null;
      profile?: Profile | undefined;
      trigger?: "signIn" | "signUp" | "update" | undefined;
      isNewUser?: boolean | undefined;
      session?: any;
    }) {
      if (profile) {
        // @ts-ignore
        token.id = profile.id;
      }
      return token;
    },
    async session({ session, token }: { session: Session; token: JWT }) {
      // @ts-ignore
      session.user.id = token.id as number;
      return session;
    },
  },
};

export default NextAuth(authOptions);
