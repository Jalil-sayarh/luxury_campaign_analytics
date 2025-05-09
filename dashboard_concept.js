import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
         LineChart, Line, PieChart, Pie, Cell, ScatterChart, Scatter, ZAxis } from 'recharts';
import { Tabs, TabList, Tab, TabPanel } from 'react-tabs';

// Sample data based on marketing_campaign_dataset.csv structure
const campaignTypes = [
  { name: 'Brand Awareness', conversionRate: 0.068, roi: 4.9, acquisitionCost: '$12.50', count: 42500 },
  { name: 'Lead Generation', conversionRate: 0.084, roi: 5.7, acquisitionCost: '$15.30', count: 38200 },
  { name: 'Product Launch', conversionRate: 0.076, roi: 5.1, acquisitionCost: '$18.20', count: 35800 },
  { name: 'Seasonal Promotion', conversionRate: 0.095, roi: 6.2, acquisitionCost: '$14.10', count: 45600 },
  { name: 'Retargeting', conversionRate: 0.110, roi: 7.4, acquisitionCost: '$11.80', count: 37900 }
];

const channelPerformance = [
  { name: 'Display', impressions: 5503, clicks: 551, conversionRate: 0.070, roi: 5.0, engagementScore: 5.51 },
  { name: 'Influencer', impressions: 5496, clicks: 548, conversionRate: 0.070, roi: 5.0, engagementScore: 5.48 },
  { name: 'Search', impressions: 5513, clicks: 549, conversionRate: 0.070, roi: 5.0, engagementScore: 5.49 },
  { name: 'Email', impressions: 5522, clicks: 549, conversionRate: 0.070, roi: 4.9, engagementScore: 5.50 },
  { name: 'Social Media', impressions: 5502, clicks: 551, conversionRate: 0.070, roi: 4.9, engagementScore: 5.50 }
];

const segmentPerformance = [
  { name: 'Fashionistas', conversionRate: 0.078, roi: 5.3, engagementScore: 5.7 },
  { name: 'Foodies', conversionRate: 0.081, roi: 5.4, engagementScore: 5.8 },
  { name: 'Tech Enthusiasts', conversionRate: 0.072, roi: 4.9, engagementScore: 5.5 },
  { name: 'Fitness Buffs', conversionRate: 0.076, roi: 5.1, engagementScore: 5.6 },
  { name: 'Budget Shoppers', conversionRate: 0.069, roi: 4.7, engagementScore: 5.3 }
];

const geographicData = [
  { name: 'North America', conversionRate: 0.082, roi: 5.5, campaignCount: 58000 },
  { name: 'Europe', conversionRate: 0.075, roi: 5.1, campaignCount: 52000 },
  { name: 'Asia Pacific', conversionRate: 0.068, roi: 4.6, campaignCount: 45000 },
  { name: 'Latin America', conversionRate: 0.064, roi: 4.3, campaignCount: 25000 },
  { name: 'Middle East', conversionRate: 0.071, roi: 4.8, campaignCount: 20000 }
];

const timeSeriesData = Array(12).fill().map((_, i) => {
  const month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i];
  return {
    name: month,
    display: 4.8 + Math.sin(i/2) * 0.7,
    influencer: 4.9 + Math.cos(i/2) * 0.6,
    search: 5.0 + Math.sin(i/2 + 1) * 0.5,
    email: 4.7 + Math.cos(i/2 + 1) * 0.4,
    socialMedia: 4.8 + Math.sin(i/2 + 2) * 0.5
  };
});

// Colors
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A569BD'];

const MarketingDashboard = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [hoveredSegment, setHoveredSegment] = useState(null);
  
  const handleTabChange = (index) => {
    setActiveTab(index);
  };

  const formatPercent = (value) => `${(value * 100).toFixed(1)}%`;
  const formatCurrency = (value) => value;

  const renderActiveShape = (props) => {
    const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill, payload, value } = props;
    
    return (
      <g>
        <text x={cx} y={cy-15} textAnchor="middle" fill="#333" fontSize={16} fontWeight="bold">
          {payload.name}
        </text>
        <text x={cx} y={cy+15} textAnchor="middle" fill="#666" fontSize={14}>
          ROI: {payload.roi.toFixed(1)}
        </text>
        <text x={cx} y={cy+35} textAnchor="middle" fill="#666" fontSize={14}>
          Conv: {formatPercent(payload.conversionRate)}
        </text>
      </g>
    );
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Marketing Campaign Analytics</h1>
        <p className="text-gray-600">Interactive dashboard showcasing campaign performance insights</p>
      </div>
      
      {/* KPI Summary */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <h3 className="text-lg font-semibold text-gray-700">Average Conversion Rate</h3>
          <p className="text-3xl font-bold text-blue-600">7.8%</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <h3 className="text-lg font-semibold text-gray-700">Average ROI</h3>
          <p className="text-3xl font-bold text-green-600">5.2</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <h3 className="text-lg font-semibold text-gray-700">Total Campaigns</h3>
          <p className="text-3xl font-bold text-purple-600">200K</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md text-center">
          <h3 className="text-lg font-semibold text-gray-700">Avg Engagement Score</h3>
          <p className="text-3xl font-bold text-orange-600">5.5</p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-800">Campaign Performance Dashboard</h2>
          <div className="flex space-x-2">
            <select className="border rounded-md px-3 py-1 text-sm">
              <option>All Companies</option>
              <option>Company A</option>
              <option>Company B</option>
              <option>Company C</option>
            </select>
            <select className="border rounded-md px-3 py-1 text-sm">
              <option>All Time</option>
              <option>2023</option>
              <option>2024</option>
              <option>Q1 2025</option>
            </select>
          </div>
        </div>
        
        <div className="space-y-1 mb-4">
          <button 
            className={`px-4 py-2 rounded-t-lg ${activeTab === 0 ? 'bg-blue-50 border-b-2 border-blue-500 font-medium' : 'text-gray-600'}`}
            onClick={() => handleTabChange(0)}
          >
            Campaign Types
          </button>
          <button 
            className={`px-4 py-2 rounded-t-lg ${activeTab === 1 ? 'bg-blue-50 border-b-2 border-blue-500 font-medium' : 'text-gray-600'}`}
            onClick={() => handleTabChange(1)}
          >
            Channel Performance
          </button>
          <button 
            className={`px-4 py-2 rounded-t-lg ${activeTab === 2 ? 'bg-blue-50 border-b-2 border-blue-500 font-medium' : 'text-gray-600'}`}
            onClick={() => handleTabChange(2)}
          >
            Customer Segments
          </button>
          <button 
            className={`px-4 py-2 rounded-t-lg ${activeTab === 3 ? 'bg-blue-50 border-b-2 border-blue-500 font-medium' : 'text-gray-600'}`}
            onClick={() => handleTabChange(3)}
          >
            Geographic Analysis
          </button>
          <button 
            className={`px-4 py-2 rounded-t-lg ${activeTab === 4 ? 'bg-blue-50 border-b-2 border-blue-500 font-medium' : 'text-gray-600'}`}
            onClick={() => handleTabChange(4)}
          >
            Time Analysis
          </button>
        </div>
        
        <div className="border-t border-gray-200 pt-4">
          {/* Campaign Types Tab */}
          {activeTab === 0 && (
            <div className="grid grid-cols-2 gap-6">
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Conversion Rate by Campaign Type</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={campaignTypes} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" tickFormatter={formatPercent} />
                    <YAxis dataKey="name" type="category" width={120} />
                    <Tooltip formatter={(value) => formatPercent(value)} />
                    <Legend />
                    <Bar dataKey="conversionRate" fill="#0088FE" name="Conversion Rate" animationDuration={1500} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">ROI by Campaign Type</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={campaignTypes}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="roi" fill="#00C49F" name="ROI" animationDuration={1500} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="h-96 col-span-2">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Campaign Distribution</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={campaignTypes}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="count"
                      nameKey="name"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      animationDuration={1500}
                    >
                      {campaignTypes.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => value.toLocaleString()} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
          
          {/* Channel Performance Tab */}
          {activeTab === 1 && (
            <div className="grid grid-cols-2 gap-6">
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Impressions vs Clicks by Channel</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={channelPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="impressions" fill="#8884d8" name="Impressions" animationDuration={1500} />
                    <Bar dataKey="clicks" fill="#82ca9d" name="Clicks" animationDuration={1500} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">ROI vs Engagement Score</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart>
                    <CartesianGrid />
                    <XAxis dataKey="roi" name="ROI" />
                    <YAxis dataKey="engagementScore" name="Engagement Score" />
                    <ZAxis range={[100, 500]} />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Legend />
                    <Scatter 
                      name="Channels" 
                      data={channelPerformance} 
                      fill="#8884d8"
                      animationDuration={1500}
                    />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
              <div className="h-96 col-span-2">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Channel Performance Comparison</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={channelPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="conversionRate" fill="#0088FE" name="Conversion Rate" animationDuration={1500} />
                    <Bar dataKey="roi" fill="#00C49F" name="ROI" animationDuration={1500} />
                    <Bar dataKey="engagementScore" fill="#FFBB28" name="Engagement Score" animationDuration={1500} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
          
          {/* Customer Segments Tab */}
          {activeTab === 2 && (
            <div className="grid grid-cols-2 gap-6">
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Segment Performance Overview</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={segmentPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="conversionRate" fill="#0088FE" name="Conversion Rate" animationDuration={1500} />
                    <Bar dataKey="roi" fill="#00C49F" name="ROI" animationDuration={1500} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Segment Engagement Analysis</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      activeIndex={hoveredSegment}
                      activeShape={renderActiveShape}
                      data={segmentPerformance}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="engagementScore"
                      onMouseEnter={(data, index) => setHoveredSegment(index)}
                      onMouseLeave={() => setHoveredSegment(null)}
                      animationDuration={1500}
                    >
                      {segmentPerformance.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="col-span-2 bg-blue-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-2 text-blue-800">Segment Insights</h3>
                <p className="text-blue-700 mb-2">
                  <span className="font-bold">Top Performing Segments:</span> Foodies and Fashionistas show the highest conversion rates and ROI.
                </p>
                <p className="text-blue-700 mb-2">
                  <span className="font-bold">Engagement Leaders:</span> Foodies demonstrate exceptional engagement scores, followed closely by Fashionistas.
                </p>
                <p className="text-blue-700">
                  <span className="font-bold">Recommendation:</span> Focus personalized campaign content on these high-performing segments to maximize marketing ROI.
                </p>
              </div>
            </div>
          )}
          
          {/* Geographic Analysis Tab */}
          {activeTab === 3 && (
            <div className="grid grid-cols-2 gap-6">
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Conversion Rate by Region</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={geographicData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" tickFormatter={formatPercent} />
                    <YAxis dataKey="name" type="category" width={120} />
                    <Tooltip formatter={(value) => formatPercent(value)} />
                    <Legend />
                    <Bar dataKey="conversionRate" fill="#0088FE" name="Conversion Rate" animationDuration={1500} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">ROI by Region</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={geographicData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="roi" fill="#00C49F" name="ROI" animationDuration={1500} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="h-96 col-span-2">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Campaign Distribution by Region</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={geographicData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="campaignCount"
                      nameKey="name"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      animationDuration={1500}
                    >
                      {geographicData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => value.toLocaleString()} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
          
          {/* Time Analysis Tab */}
          {activeTab === 4 && (
            <div className="grid grid-cols-1 gap-6">
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-2 text-gray-700">Channel ROI Over Time</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={timeSeriesData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="display" stroke="#8884d8" name="Display" activeDot={{ r: 8 }} animationDuration={1500} />
                    <Line type="monotone" dataKey="influencer" stroke="#82ca9d" name="Influencer" animationDuration={1500} />
                    <Line type="monotone" dataKey="search" stroke="#ffc658" name="Search" animationDuration={1500} />
                    <Line type="monotone" dataKey="email" stroke="#ff8042" name="Email" animationDuration={1500} />
                    <Line type="monotone" dataKey="socialMedia" stroke="#a569bd" name="Social Media" animationDuration={1500} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="grid grid-cols-2 gap-6">
                <div className="bg-green-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold mb-2 text-green-800">Seasonal Trends</h3>
                  <p className="text-green-700 mb-2">
                    <span className="font-bold">Peak Performance:</span> Display and Influencer campaigns show strongest ROI during Q2 and Q4.
                  </p>
                  <p className="text-green-700 mb-2">
                    <span className="font-bold">Consistent Channels:</span> Search maintains the most consistent performance throughout the year.
                  </p>
                  <p className="text-green-700">
                    <span className="font-bold">Recommendation:</span> Allocate higher budget to Display and Influencer channels during peak seasons.
                  </p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold mb-2 text-purple-800">Campaign Duration Insights</h3>
                  <p className="text-purple-700 mb-2">
                    <span className="font-bold">Optimal Duration:</span> Medium-length campaigns (2-4 weeks) show the highest average ROI.
                  </p>
                  <p className="text-purple-700 mb-2">
                    <span className="font-bold">Channel Differences:</span> Email campaigns perform better with longer durations, while Display shows stronger short-term results.
                  </p>
                  <p className="text-purple-700">
                    <span className="font-bold">Recommendation:</span> Tailor campaign duration to channel strategy for maximum effectiveness.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Key Insights Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Key Strategic Insights</h2>
        <div className="grid grid-cols-3 gap-6">
          <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
            <h3 className="text-lg font-semibold mb-2 text-blue-800">Channel Optimization</h3>
            <p className="text-blue-700">
              Display and Influencer campaigns demonstrate the highest ROI and engagement scores. These channels should receive increased investment to maximize returns.
            </p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
            <h3 className="text-lg font-semibold mb-2 text-green-800">Segment Targeting</h3>
            <p className="text-green-700">
              Campaigns tailored to the Fashionistas and Foodies audience segments have shown higher conversion rates. Focus on creating personalized content for these segments.
            </p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
            <h3 className="text-lg font-semibold mb-2 text-purple-800">Geographic Focus</h3>
            <p className="text-purple-700">
              North America shows the highest conversion rates and ROI. Consider reallocating budget to prioritize this region while optimizing underperforming regions.
            </p>
          </div>
        </div>
      </div>
      
      {/* Interactive What-If Analysis */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Budget Allocation Simulator</h2>
        <p className="text-gray-600 mb-4">Adjust the budget allocation sliders to see the projected impact on overall campaign performance.</p>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Display</label>
              <input type="range" min="0" max="100" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" defaultValue="25" />
              <div className="flex justify-between text-xs text-gray-500">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Influencer</label>
              <input type="range" min="0" max="100" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" defaultValue="20" />
              <div className="flex justify-between text-xs text-gray-500">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
              <input type="range" min="0" max="100" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" defaultValue="15" />
              <div className="flex justify-between text-xs text-gray-500">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input type="range" min="0" max="100" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" defaultValue="15" />
              <div className="flex justify-between text-xs text-gray-500">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Social Media</label>
              <input type="range" min="0" max="100" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" defaultValue="25" />
              <div className="flex justify-between text-xs text-gray-500">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold mb-4 text-gray-800">Projected Performance</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white p-3 rounded border border-gray-200">
                <p className="text-sm text-gray-600">Estimated Conversion Rate</p>
                <p className="text-2xl font-bold text-blue-600">8.2%</p>
                <p className="text-xs text-green-600">+0.4% from current</p>
              </div>
              <div className="bg-white p-3 rounded border border-gray-200">
                <p className="text-sm text-gray-600">Projected ROI</p>
                <p className="text-2xl font-bold text-green-600">5.6</p>
                <p className="text-xs text-green-600">+0.4 from current</p>
              </div>
              <div className="bg-white p-3 rounded border border-gray-200">
                <p className="text-sm text-gray-600">Expected Engagement</p>
                <p className="text-2xl font-bold text-purple-600">5.7</p>
                <p className="text-xs text-green-600">+0.2 from current</p>
              </div>
              <div className="bg-white p-3 rounded border border-gray-200">
                <p className="text-sm text-gray-600">Acquisition Cost</p>
                <p className="text-2xl font-bold text-orange-600">$14.20</p>
                <p className="text-xs text-green-600">-$1.10 from current</p>
              </div>
            </div>
            <div className="mt-6">
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition duration-300">
                Generate Detailed Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketingDashboard;