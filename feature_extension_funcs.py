#------------------------NEW FEATURES-------------------------------
def title_name(df):
    '''
    INPUT  : ['name']
    OUTPUT : ['title'] 
    
    Extract title and surname from 'name' feature.
    Rare titles are combined with common titles:
    - Mr.   = Dr.+Rev.+Don.
    - Mrs.  = Ms.+ Mme.
    - Miss. = Mlle.+Ms.(even not clear mariage status, more Miss. exist)
    - VIP   = Major.+Lady.+Sir.+Col.+the Countess.+Jonkheer. 
    '''    
   
    df['title'] = df['name'].apply(lambda x: x.split(',')[1].strip().split(' ')[0])
    df['surname'] = df['name'].apply(lambda x: x.split(',')[0])           
    
    # Modify titles 
    df.loc[df['title'].isin(['Mme.']), 'title']                                               = 'Mrs.'
    df.loc[df['title'].isin(['Mlle.','Ms.']), 'title']                                        = 'Miss.'
    df.loc[df['title'].isin(['Dr.', 'Rev.', 'Don.']), 'title']                                = 'Mr.'
    df.loc[df['title'].isin(['Major.', 'Lady.', 'Sir.', 'Col.', 'the', 'Jonkheer.']),'title'] = 'Vip.'
    
    df.drop(columns='name')
    return df
    
def define_groups(df):
    '''
    INPUT  : ['sibsp','parch']
    OUTPUT : ['famsize', 'grpsize']
    
    -Calculate (famsize) number of family members of all passengers. 
    -There are some friend groups. So one should check if there are different surnames in same ticket.
    '''
    df['famsize'] = df['sibsp']+df['parch']+1    
    df2 = df.groupby(['ticket','surname'])['famsize'].mean().groupby('ticket').sum().reset_index()
    df  = df.merge(df2, how='left', on='ticket')
    
    df.rename(columns={"famsize_x": "famsize", "famsize_y": "grpsize"}, inplace=True)
    
    df.drop(columns=['sibsp','parch'])
    return df
    
def prices(df):
    '''
    INPUT  : ['fare', 'famsize']
    OUTPUT : ['price']
    
    The tickets for multiple passengers show total price (It shown in Fare section). Calculate price per person for given fares. 
    (Assume that all families are on board and share same tickets! Can not calculate from 'fare' because data is alreadz train/test split)
    '''
    
    df['price'] = (df['fare'] / df['grpsize']).astype('int64')
    
    df.drop(columns='fare')
    return df


#------------------------IMPUTATION-------------------------------
def cabin_filled (df):
    df['cabin_f_cat'] = df['cabin'].fillna(value=0)
    df.loc[df['cabin_f_cat']!=0, 'cabin_f_cat'] = 1
    df.drop(columns='cabin')
    return df
    
def embarked_filled (df):
    df.loc[df['embarked'].isna(), 'embarked'] = 'S'
    df['emb_fill']=df['embarked']
    df.drop(columns='embarked')
    return df
   
def age_groups(df):
    '''
    INPUT  : ['age']
    OUTPUT : ['age_group']
    
    -Define passengers age groups: 'age_group'
    ''' 
    
    df['age_group'] = 0
    df.loc[(df['age'] >  8), 'age_group']                     = 1
    df.loc[(df['age'] >= 8)  & (df['age'] < 19), 'age_group'] = 2
    df.loc[(df['age'] >= 19) & (df['age'] < 51), 'age_group'] = 3
    df.loc[(df['age'] >= 51) & (df['age'] < 66), 'age_group'] = 4
    df.loc[(df['age'] >= 66),'age_group']                     = 5

    return df
    
def age_filled_tit (df):
    df['age_filled_tit'] = df['age']
    df.loc[(df['age_filled_tit'].isna()) & (df['title']=='Mr.'), 'age_filled_tit']     = df.loc[df['title'] == 'Mr.']['age_filled_tit'].median()
    df.loc[(df['age_filled_tit'].isna()) & (df['title']=='Miss.'), 'age_filled_tit']   = df.loc[df['title'] == 'Miss.']['age_filled_tit'].median()
    df.loc[(df['age_filled_tit'].isna()) & (df['title']=='Mrs.'), 'age_filled_tit']    = df.loc[df['title'] == 'Mrs.']['age_filled_tit'].median()
    df.loc[(df['age_filled_tit'].isna()) & (df['title']=='Master.'), 'age_filled_tit'] = df.loc[df['title'] == 'Master.']['age_filled_tit'].median()
    
    return df