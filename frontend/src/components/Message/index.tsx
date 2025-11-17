import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'lucide-react';
import type { Message as MessageType } from '../../types';

interface MessageProps {
  message: MessageType;
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const [copiedCode, setCopiedCode] = React.useState<string | null>(null);

  const handleCopyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(code);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  return (
    <div
      className="py-6 px-4 animate-fade-in"
      style={{
        backgroundColor:
          message.role === 'assistant'
            ? 'var(--color-background-secondary)'
            : 'transparent',
      }}
    >
      <div className="max-w-4xl mx-auto">
        {/* Role Label */}
        <div
          className="text-xs font-semibold mb-2"
          style={{
            color:
              message.role === 'user'
                ? 'var(--color-primary)'
                : 'var(--color-success)',
          }}
        >
          {message.role === 'user' ? 'You' : 'Assistant'}
        </div>

        {/* Message Content */}
        <div className="markdown-content">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({ node, inline, className, children, ...props }: any) {
                const match = /language-(\w+)/.exec(className || '');
                const codeString = String(children).replace(/\n$/, '');

                if (!inline && match) {
                  return (
                    <div className="relative group">
                      <button
                        onClick={() => handleCopyCode(codeString)}
                        className="absolute top-2 right-2 p-2 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                        style={{
                          backgroundColor: 'var(--color-background-hover)',
                          color: 'var(--color-text-primary)',
                        }}
                        title="Copy code"
                      >
                        {copiedCode === codeString ? (
                          <Check size={16} style={{ color: 'var(--color-success)' }} />
                        ) : (
                          <Copy size={16} />
                        )}
                      </button>
                      <SyntaxHighlighter
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        customStyle={{
                          margin: 0,
                          borderRadius: 'var(--radius-md)',
                          backgroundColor: 'var(--color-code-background)',
                        }}
                        {...props}
                      >
                        {codeString}
                      </SyntaxHighlighter>
                    </div>
                  );
                }

                return (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Timestamp */}
        <div
          className="text-xs mt-2"
          style={{ color: 'var(--color-text-tertiary)' }}
        >
          {new Date(message.created_at).toLocaleString()}
        </div>
      </div>
    </div>
  );
};
