/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  rewrites: async () => {
    return [
      {
        source: '/api/chat/:path*',
        destination: process.env.NODE_ENV === 'development' 
          ? 'http://127.0.0.1:8000/api/chat/:path*'
          : '/api/chat/:path*',
      },
    ];
  },
};

module.exports = nextConfig; 