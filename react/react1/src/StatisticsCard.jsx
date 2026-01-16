import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const StatisticsCard = () => {
  const visitorData = [
    { year: '2023', visitors: 5000 }, 
    { year: '2024', visitors: 7700 },
    { year: '2025', visitors: 9500 },
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-4xl">
        {/* Title Section */}
        <div className="border-b-4 border-blue-600 pb-4 mb-6">
          <h1 className="text-2xl font-bold text-gray-800">港人北上消費趨勢 (2024–2025數據)</h1>
          <h2 className="text-lg text-gray-600 mt-2">港人北上已成常態，坪山迎重大機遇</h2>
        </div>

        {/* Chart Section */}
        <div className="mb-6">
          <h3 className="text-lg font-bold mb-4 text-gray-700">出入境人次增長</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={visitorData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="visitors" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bottom Text */}
        <p className="text-sm text-gray-500 text-center">
          2025年深圳口岸出入境總量超2.73億人次
        </p>

        {/* Pagination */}
        <div className="flex items-center justify-center mt-6 space-x-4">
          <button className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <span className="text-sm text-gray-600">3 / 13</span>
          <button className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default StatisticsCard;
