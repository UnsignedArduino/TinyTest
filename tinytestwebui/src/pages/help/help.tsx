import Link from "next/link";
import React from "react";
import Layout from "../../components/Layout";
import getAppProps, { AppProps } from "../../components/WithAppProps";

const pageName = "Help";

export function Help({ appProps }: { appProps: AppProps }): JSX.Element {
  const helpPages = {
    Legal: "/legal",
  };

  return (
    <Layout
      title={pageName}
      currentPage={pageName}
      appProps={appProps}
      description="TinyTest's help page."
      keywords="TinyTest, Chess, Engine, Chess engine, Chess engine testing, Testing, Distributed, Help, Help page, Main help page"
    >
      <h1>{pageName}</h1>
      <ul>
        {Object.entries(helpPages).map(([name, page]) => {
          return (
            <li key={name}>
              <Link href={page.startsWith("/") ? page : `/help/${page}`}>
                {name}
              </Link>
            </li>
          );
        })}
      </ul>
      <p>
        If you have any problems, you can join me on{" "}
        <a
          href="https://github.com/UnsignedArduino/TinyTest/discussions"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub Discussions
        </a>
        .
      </p>
    </Layout>
  );
}

export async function getStaticProps(): Promise<{
  props: { appProps: AppProps };
}> {
  return {
    props: {
      appProps: await getAppProps(),
    },
  };
}

export default Help;
