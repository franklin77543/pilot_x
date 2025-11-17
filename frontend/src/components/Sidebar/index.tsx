import React from 'react';
import { MessageSquare, Plus, Edit2, Trash2 } from 'lucide-react';
import { useStore } from '../../store';
import { conversationApi } from '../../services/api';
import type { Conversation } from '../../types';

export const Sidebar: React.FC = () => {
  const {
    conversations,
    currentConversation,
    setCurrentConversation,
    addConversation,
    updateConversation,
    deleteConversation,
    setMessages,
    setError,
  } = useStore();

  const [editingId, setEditingId] = React.useState<string | null>(null);
  const [editTitle, setEditTitle] = React.useState('');

  const handleNewChat = async () => {
    try {
      const newConv = await conversationApi.create();
      addConversation(newConv);
      setCurrentConversation(newConv);
      setMessages([]);
    } catch (error) {
      setError('Failed to create new conversation');
      console.error('Error creating conversation:', error);
    }
  };

  const handleSelectConversation = (conv: Conversation) => {
    setCurrentConversation(conv);
    setMessages([]);
  };

  const handleStartEdit = (conv: Conversation, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingId(conv.id);
    setEditTitle(conv.title);
  };

  const handleSaveEdit = async (id: string) => {
    if (!editTitle.trim()) return;
    
    try {
      await conversationApi.update(id, editTitle);
      updateConversation(id, { title: editTitle });
      setEditingId(null);
    } catch (error) {
      setError('Failed to update conversation');
      console.error('Error updating conversation:', error);
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditTitle('');
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Delete this conversation?')) return;

    try {
      await conversationApi.delete(id);
      deleteConversation(id);
    } catch (error) {
      setError('Failed to delete conversation');
      console.error('Error deleting conversation:', error);
    }
  };

  return (
    <div className="flex flex-col h-full" style={{ backgroundColor: 'var(--color-background-secondary)' }}>
      {/* Header */}
      <div className="p-4 border-b" style={{ borderColor: 'var(--color-border)' }}>
        <button
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 rounded transition-colors"
          style={{
            backgroundColor: 'var(--color-primary)',
            color: 'var(--color-text-inverse)',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--color-primary-hover)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--color-primary)';
          }}
        >
          <Plus size={18} />
          <span className="font-medium">New Chat</span>
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {conversations.map((conv) => (
          <div
            key={conv.id}
            className="group relative flex items-center gap-2 px-4 py-3 cursor-pointer transition-colors border-b"
            style={{
              backgroundColor:
                currentConversation?.id === conv.id
                  ? 'var(--color-background-active)'
                  : 'transparent',
              borderColor: 'var(--color-border)',
            }}
            onClick={() => handleSelectConversation(conv)}
            onMouseEnter={(e) => {
              if (currentConversation?.id !== conv.id) {
                e.currentTarget.style.backgroundColor = 'var(--color-background-hover)';
              }
            }}
            onMouseLeave={(e) => {
              if (currentConversation?.id !== conv.id) {
                e.currentTarget.style.backgroundColor = 'transparent';
              }
            }}
          >
            <MessageSquare size={16} style={{ color: 'var(--color-text-secondary)' }} />
            
            {editingId === conv.id ? (
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                onBlur={() => handleSaveEdit(conv.id)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleSaveEdit(conv.id);
                  if (e.key === 'Escape') handleCancelEdit();
                }}
                className="flex-1 px-2 py-1 text-sm rounded"
                style={{
                  backgroundColor: 'var(--color-background-primary)',
                  color: 'var(--color-text-primary)',
                  border: '1px solid var(--color-border-focus)',
                }}
                autoFocus
                onClick={(e) => e.stopPropagation()}
              />
            ) : (
              <span className="flex-1 text-sm truncate" style={{ color: 'var(--color-text-primary)' }}>
                {conv.title}
              </span>
            )}

            <div className="hidden group-hover:flex items-center gap-1">
              <button
                onClick={(e) => handleStartEdit(conv, e)}
                className="p-1 rounded transition-colors"
                style={{ color: 'var(--color-text-secondary)' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = 'var(--color-background-hover)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent';
                }}
              >
                <Edit2 size={14} />
              </button>
              <button
                onClick={(e) => handleDelete(conv.id, e)}
                className="p-1 rounded transition-colors"
                style={{ color: 'var(--color-text-secondary)' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = 'var(--color-background-hover)';
                  e.currentTarget.style.color = 'var(--color-error)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.color = 'var(--color-text-secondary)';
                }}
              >
                <Trash2 size={14} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
