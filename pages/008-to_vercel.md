Maintaining infrastructure by yourself is always a boring job, especially when it comes to https certificate related work and nginx configuration.

The original domain name of this site is _.0xffff.me, and I didn't want to spend too much time on writing the front-end code, so I made it quickly with some very old unix tools and some shell script, I record them in this post [https://me.0xffff.me/suckless.html](https://me.0xffff.me/suckless.html).

But after being mentioned more than once by friends about the lack of https and my weird domain name that didn't resolve on Twitter, I finally made up my mind to embrace the modern world (well, my friend [@rauchg](twitter.com/rauchg) also gave me the motivation).

I know Vercel has good support for the Next.js (and some other modern Web Frameworks) ecosystem, but I'm not sure if it supports such fully customizable and raw static sites. In the end, though, the jounrney turned out to be quite simple. 

My goal: to learn as few new concepts as possible and get the job done (I don't like reading docs...no one like)

After registering for a Vercel account, after signing up, it's natural to notice that it implements the GitOps concept very well, and your work will revolve around your git repo, which is very nice and easy. I can do that.

Then, I directly put my repo URL into it, the automated build begins, Naturally, I didn't have any hints to let Vercel know how my site was building, so the first build failed, but it's good that the build log can clearly see what vercel is trying to do.

To be honest, I think Vercel's Project Setting is a little bit hard to find, and it took me a long time to find a way to get Vercel to let me custom build step, but it was through Google: [https://vercel.com/guides/how-can-i-add-a-custom-build-step-to-my-project](https://vercel.com/guides/how-can-i-add-a-custom-build-step-to-my-project)

I noticed some custom scripts mentioned in this article, and I found a file called package.json to be important. This reminds me of npm. A very reasonable guess is that Vercel will run `npm run build` I can put my build script in package.json, this conjecture proved to be correct. But then when I found the project settings page, it all became clear.

<pre>
{
  "scripts": {
        "build": "pushd ./build; sh build.sh; popd"
    }
}
</pre>

The second challenge was to prepare the build environment. There were some minor roadblocks here, such as wget is not in the VM, but since there was a package manager, this didn't block me for long.

What made me unhappy was that even if I made some small changes, I had to git push to the remote and then Vercel would start a new building. It was a pain not to have a debugging environment locally, especially for some complex build processes. This is not only a problem for Vercel, I had the same pain when using Github Action. 

The third problem is where should the generated directoy be put for Vercel to render it? Like I said, I try to avoid reading the documentation. 

This is something that Vercel does very well, outputting the clue in the build log directly after finishing the build

`Error: No Output Directory named "public" found after the Build completed. You can configure the Output Directory in your Project Settings.`

So it is a reasonable guess that Vercel will render the contents of the public/ folder (as long as it has index.html). My guess was right, and after I renamed the output directory from output/ to public/, my site was up and running.

The journey that follows is the domain name, setting the domain name in Vercel is basically no-brainer, simply add a CNAME, https? not even a problem, I didn't do anything, Vercel just correctly setup for my site.

Basically everything was done, I had set aside about 3 hours for the migration(Like I said, I'm not familiar with modern front-end development), but everything took me about 30min. During this process, I can feel Vercel's focus on the development journey and make it as easy as possible, which is pretty good.

Next I'll try to migrate some dynamic applications I've written to Vercel, as well as use TiDB Serverless for the backend storage (TiDB is an official Vercel partner and I'm proud of it), stay tuned!





