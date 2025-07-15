import { ShieldCheck, AlertTriangle } from 'lucide-react'

export default function Header() {
  return (
    <div className="text-center mb-8">
      <div className="flex justify-center items-center mb-4">
        <ShieldCheck className="h-12 w-12 text-blue-600 mr-3" />
        <h1 className="text-4xl font-bold text-gray-800">Health Fact Checker</h1>
      </div>
      
      <p className="text-lg text-gray-600 mb-4">
        AI-powered nutritional fact verification for health products
      </p>
      
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-center mb-2">
          <AlertTriangle className="h-5 w-5 text-yellow-600 mr-2" />
          <span className="font-semibold text-yellow-800">Important Disclaimer</span>
        </div>
        <p className="text-sm text-yellow-700">
          This tool provides educational information only and should not replace professional medical advice. 
          Always consult with healthcare professionals before making health-related decisions.
        </p>
      </div>
    </div>
  )
} 